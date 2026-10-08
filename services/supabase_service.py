# services/supabase_service.py

from supabase import create_client, Client


class SupabaseClient:
    def __init__(self, url, key, table_name):
        if not url or not key:
            raise ValueError("Supabase URL and Key must be provided.")

        self.client: Client = create_client(url, key)
        self.table_name = table_name

    def insert_random_name(self, random_name):
        data = {'name': random_name}

        try:
            response = (
                self.client
                .table(self.table_name)
                .insert(data)
                .execute()
            )

            print(
                f"Inserted data into '{self.table_name}': "
                f"{response.data}"
            )

            return True

        except Exception as e:
            print(
                f"Error inserting data into "
                f"'{self.table_name}': {e}"
            )
            return False

    def get_table_count(self):
        try:
            response = (
                self.client
                .table(self.table_name)
                .select('*', count='exact')
                .execute()
            )

            if response.count is not None:
                return response.count

            print(
                f"Could not retrieve count from "
                f"'{self.table_name}'."
            )
            return None

        except Exception as e:
            print(
                f"Error counting data in "
                f"'{self.table_name}': {e}"
            )
            return None

    def delete_old_entries(self, count):
        """
        Delete the oldest entries based on their ID.

        Args:
            count: Number of old entries to delete.

        Returns:
            True if deletion succeeds, False otherwise.
        """

        try:
            if count <= 0:
                print("No entries need to be deleted.")
                return True

            # Get IDs ordered from oldest to newest
            response = (
                self.client
                .table(self.table_name)
                .select('id')
                .order('id', desc=False)
                .execute()
            )

            if not response.data:
                print(
                    f"No entries found in "
                    f"'{self.table_name}'."
                )
                return True

            # Select the oldest IDs
            old_ids = [
                item['id']
                for item in response.data[:count]
            ]

            if not old_ids:
                print("No old entries to delete.")
                return True

            # Delete all selected old entries
            self.client \
                .table(self.table_name) \
                .delete() \
                .in_('id', old_ids) \
                .execute()

            print(
                f"Deleted {len(old_ids)} old entries "
                f"from '{self.table_name}': {old_ids}"
            )

            return True

        except Exception as e:
            print(
                f"Error deleting old entries "
                f"from '{self.table_name}': {e}"
            )
            return False

    def delete_random_entry(self):
        try:
            # Fetch all IDs from the table
            response = (
                self.client
                .table(self.table_name)
                .select('id')
                .execute()
            )

            if response.data:
                ids = [item['id'] for item in response.data]

                if not ids:
                    print(
                        f"No entries to delete in "
                        f"'{self.table_name}'."
                    )
                    return True

                # Randomly select one ID to delete
                import random
                random_id = random.choice(ids)

                # Delete the selected entry
                (
                    self.client
                    .table(self.table_name)
                    .delete()
                    .eq('id', random_id)
                    .execute()
                )

                print(
                    f"Deleted entry with id {random_id} "
                    f"from '{self.table_name}'."
                )

                return True

            else:
                print(
                    f"No data retrieved from "
                    f"'{self.table_name}'."
                )
                return False

        except Exception as e:
            print(
                f"Error deleting data from "
                f"'{self.table_name}': {e}"
            )
            return False
