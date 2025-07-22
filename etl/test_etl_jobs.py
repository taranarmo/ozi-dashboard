import unittest
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime
from main import (
    etl_load_asns,
    etl_load_stats_1d,
    etl_load_stats_5m,
    etl_load_asn_neighbours,
    etl_load_traffic,
    etl_load_internet_quality,
)


class TestETLJobs(unittest.TestCase):
    # Test etl_load_asns
    @patch("etl_script.insert_country_asns_to_db")  # Mock DB insert function
    @patch("etl_script.get_list_of_asns_for_country")  # Mock API/data-fetch function
    def test_etl_load_asns(self, mock_get_asns, mock_insert_asns):
        iso2 = "US"
        dates = ["2023-01-01", "2023-01-02"]

        # Simulate two batches of ASN data being returned by the data source
        mock_get_asns.return_value = [["ASN1", "ASN2"], ["ASN3"]]

        # Run the ETL job
        etl_load_asns(iso2, dates)

        # Check if the API was called with expected arguments
        mock_get_asns.assert_called_once_with(iso2, dates, ANY)

        # The insert function should be called once for each batch
        self.assertEqual(mock_insert_asns.call_count, 2)
        mock_insert_asns.assert_any_call(iso2, ["ASN1", "ASN2"])
        mock_insert_asns.assert_any_call(iso2, ["ASN3"])

    # Test etl_load_stats_1d
    @patch("etl_script.insert_country_stats_to_db")
    @patch("etl_script.get_stats_for_country")
    def test_etl_load_stats_1d(self, mock_get_stats, mock_insert_stats):
        iso2 = "DE"
        dates = [datetime(2023, 1, 1), datetime(2023, 1, 2)]

        # Simulate one day with data and one day with no data
        mock_get_stats.side_effect = [[{"stat": 1}], None]

        etl_load_stats_1d(iso2, dates)

        # The data fetching function should be called once per date
        self.assertEqual(mock_get_stats.call_count, 2)

        # The insert function should only be called for the day with data
        mock_insert_stats.assert_called_once_with(iso2, "1d", [{"stat": 1}], True)

    # Test etl_load_stats_5m
    @patch("etl_script.insert_country_stats_to_db")
    @patch("etl_script.get_stats_for_country")
    def test_etl_load_stats_5m(self, mock_get_stats, mock_insert_stats):
        iso2 = "FR"
        dates = [datetime(2023, 1, 1)]

        # Simulate data being returned
        mock_get_stats.return_value = [{"stat": "some"}]

        etl_load_stats_5m(iso2, dates)

        # Check correct API call
        mock_get_stats.assert_called_once_with(iso2, dates[0], dates[0], "5m")

        # Check correct DB insert
        mock_insert_stats.assert_called_once_with(iso2, "5m", [{"stat": "some"}], True)

    # Test etl_load_asn_neighbours
    @patch("etl_script.insert_country_asn_neighbours_to_db")
    @patch("etl_script.get_list_of_asn_neighbours_for_country")
    def test_etl_load_asn_neighbours(self, mock_get_neigh, mock_insert_neigh):
        iso2 = "JP"
        dates = ["2023-01-01", "2023-01-02"]

        # Simulate two batches of ASN neighbour data
        mock_get_neigh.return_value = [["N1", "N2"], ["N3"]]

        etl_load_asn_neighbours(iso2, dates)

        # Ensure the data source is queried with correct parameters
        mock_get_neigh.assert_called_once_with(iso2, dates, ANY)

        # Ensure data is inserted in two separate calls
        self.assertEqual(mock_insert_neigh.call_count, 2)
        mock_insert_neigh.assert_any_call(iso2, ["N1", "N2"])
        mock_insert_neigh.assert_any_call(iso2, ["N3"])

    # Test etl_load_traffic
    @patch("etl_script.insert_traffic_for_country_to_db")
    @patch("etl_script.get_traffic_for_country")
    def test_etl_load_traffic(self, mock_get_traffic, mock_insert_traffic):
        iso2 = "BR"
        dates = ["2023-01-01"]  # not used in the actual function, but passed anyway

        # Simulate returned traffic data
        mock_get_traffic.return_value = {"traffic": "some_data"}

        etl_load_traffic(iso2, dates)

        # Check API was called with token (mocked by ANY)
        mock_get_traffic.assert_called_once_with(iso2, ANY)

        # Ensure traffic is inserted into DB correctly
        mock_insert_traffic.assert_called_once_with(
            iso2, {"traffic": "some_data"}, True
        )

    # Test etl_load_internet_quality
    @patch("etl_script.insert_internet_quality_for_country_to_db")
    @patch("etl_script.get_internet_quality_for_country")
    def test_etl_load_internet_quality(self, mock_get_quality, mock_insert_quality):
        iso2 = "IN"
        dates = ["2023-01-01"]

        # Simulate internet quality data being returned
        mock_get_quality.return_value = {"latency": 42}

        etl_load_internet_quality(iso2, dates)

        # Check that the correct API call was made
        mock_get_quality.assert_called_once_with(iso2, ANY)

        # Ensure the data is inserted correctly
        mock_insert_quality.assert_called_once_with(iso2, {"latency": 42}, True)


# Allows running the test file directly with: python test_etl_jobs.py
if __name__ == "__main__":
    unittest.main()
