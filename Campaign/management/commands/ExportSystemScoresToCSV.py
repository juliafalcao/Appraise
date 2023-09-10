# pylint: disable=C0103,C0111,C0330,E1101
import sys
import pandas as pd
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import User

from Campaign.models import *
from EvalData.models import *
from Dashboard.models import LANGUAGE_CODES_AND_NAMES, LANGUAGE_PAIRS, PROFICIENCY_LEVELS

CAMPAIGN_TASK_PAIRS = {(tup[1], tup[2]) for tup in TASK_DEFINITIONS}


class Command(BaseCommand):
    help = 'Exports system scores over all results to CSV format'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            help='Directory to put the output files',
        )


    def handle(self, *args, **options):

        # create timestamp for the filenames
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")

        # check output-dir
        output_path = options["output_dir"]
        # print("Output directory:", output_path)

        if not os.path.isdir(output_path):
            raise CommandError("The given output directory does not exist.")

        # list campaigns
        all_campaigns = Campaign.objects.all()
        dfs_scores = []

        # loop over campaigns
        for campaign in all_campaigns:
            # print(f"Querying results for campaign `{campaign}`...")

            # query result scores
            system_scores = []

            for task_cls, result_cls in CAMPAIGN_TASK_PAIRS:
                qs_name = task_cls.__name__.lower()
                qs_attr = f"evaldata_{qs_name}_campaign"
                qs_obj = getattr(campaign, qs_attr, None)

                if qs_obj and qs_obj.exists():
                    _scores = result_cls.get_system_data(
                        campaign.id,
                        extended_csv=True,
                        add_batch_info=True,
                    )
                    system_scores.extend(_scores)

            # if len(system_scores) == 0:
                # print(f"No results found in campaign `{campaign.campaignName}`.")

            # put the scores in a DF
            columns = ["username", "targetID", "itemID", "itemType", "src", "tgt", "score", "startTime", "endTime", "batchNo", "realItemID"]
            df_scores = pd.DataFrame(system_scores, columns=columns)
            # print("Scores found:", len(df_scores))

            # create extra fields
            df_scores["deltaTime"] = df_scores.endTime - df_scores.startTime
            df_scores["campaign"] = campaign.campaignName

            # print(df_scores.head().to_string())

            # add to list of DFs per campaign
            dfs_scores.append(df_scores)


        # join all the df_scores of each campaign
        df_scores = pd.concat(dfs_scores, ignore_index=True)

        # save scores DF to CSV
        output_scores_path = os.path.join(output_path, f"results.{timestamp}.csv")
        df_scores.to_csv(output_scores_path, index=False)
        # print(f"Scores saved to `{output_scores_path}`.")

        # query the users responsible for these scores to get language information
        unique_users = df_scores.username.unique().tolist()
        user_objects = User.objects.filter(username__in=unique_users)

        # aux function that takes an username and the query result for this User object and returns the language information
        def parse_groups(username, user_query_result):
            user_dict = {
                "username": username,
            }

            group_names = [group_obj.name for group_obj in user_query_result.groups.all()]

            # find source and target languages they're working with
            for src, tgt in LANGUAGE_PAIRS:
                if src in group_names and tgt in group_names:
                    user_dict["src"] = src
                    user_dict["tgt"] = tgt

                    # find their corresponding proficiency level in each language
                    for proficiency_level in PROFICIENCY_LEVELS:
                        if f"{src}-{proficiency_level}" in group_names:
                            user_dict["src_level"] = proficiency_level
                        if f"{tgt}-{proficiency_level}" in group_names:
                            user_dict["tgt_level"] = proficiency_level

            return user_dict

        # get the dicts for all the unique users in the results
        rows = [parse_groups(username, queryset) for (username, queryset) in zip(unique_users, user_objects)]
        
        # store in dataframe and save to CSV
        df_users = pd.DataFrame(rows)
        # print("Unique users:", len(df_users))
        # print(df_users.head().to_string())

        output_users_path =  os.path.join(output_path, f"users.{timestamp}.csv")
        df_users.to_csv(output_users_path, index=False)
        # print(f"Users saved to `{output_users_path}`.")
