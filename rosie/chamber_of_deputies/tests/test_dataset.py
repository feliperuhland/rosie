import os.path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import patch
from shutil import copy2

from rosie.chamber_of_deputies.dataset import Dataset


class TestDataset(TestCase):

    def setUp(self):
        temp_path = mkdtemp()
        copy2('rosie/chamber_of_deputies/tests/fixtures/companies.xz',
              os.path.join(temp_path, Dataset.COMPANIES_DATASET))
        copy2('rosie/chamber_of_deputies/tests/fixtures/reimbursements.xz', temp_path)
        self.subject = Dataset(temp_path)

    @patch('rosie.chamber_of_deputies.dataset.CEAPDataset')
    @patch('rosie.chamber_of_deputies.dataset.fetch')
    def test_get_performs_a_left_merge_between_reimbursements_and_companies(self, _ceap_dataset, _fetch):
        dataset = self.subject.get()
        self.assertEqual(5, len(dataset))
        self.assertEqual(1, dataset['legal_entity'].isnull().sum())
