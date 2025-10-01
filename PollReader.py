import os
import unittest


class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        The constructor. Opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().

        We have implemented this for you. You should not need to modify it.
        """

        # this is used to get the base path that this Python file is in in an
        # OS agnostic way since Windows and Mac/Linux use different formats
        # for file paths, the os library allows us to write code that works
        # well on any operating system
        self.base_path = os.path.abspath(os.path.dirname(__file__))

        # join the base path with the passed filename
        self.full_path = os.path.join(self.base_path, filename)

        # open up the file handler
        self.file_obj = open(self.full_path, 'r')

        # read in each line of the file to a list
        self.raw_data = self.file_obj.readlines()

        # close the file handler
        self.file_obj.close()

        # set up the data dict that we will fill in later
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
    # Skip the header row (first line)
        for line in self.raw_data[1:]:
            separated = line.strip().split(',')

            self.data_dict['month'].append(separated[0])
            self.data_dict['date'].append(int(separated[1]))

        # Split "sample" column into number + type
            sample_parts = separated[2].split()
            self.data_dict['sample'].append(int(sample_parts[0]))
            self.data_dict['sample type'].append(sample_parts[1])

            self.data_dict['Harris result'].append(float(separated[3]))
            self.data_dict['Trump result'].append(float(separated[4]))


    def highest_polling_candidate(self):
        max_harris = max(self.data_dict['Harris result'])
        max_trump = max(self.data_dict['Trump result'])

        if max_harris > max_trump:
            return f"Harris {max_harris:.1%}"
        elif max_trump > max_harris:
            return f"Trump {max_trump:.1%}"
        else:
            return f"EVEN {max_harris:.1%}"
    


    def likely_voter_polling_average(self):
        harris_lv = [h for h, t, st in zip(self.data_dict['Harris result'],
                                       self.data_dict['Trump result'],
                                       self.data_dict['sample type']) if st == "LV"]

        trump_lv = [t for h, t, st in zip(self.data_dict['Harris result'],
                                      self.data_dict['Trump result'],
                                      self.data_dict['sample type']) if st == "LV"]

        harris_avg = sum(harris_lv) / len(harris_lv)
        trump_avg = sum(trump_lv) / len(trump_lv)

        return harris_avg, trump_avg

    def polling_history_change(self):
        harris = self.data_dict['Harris result']
        trump = self.data_dict['Trump result']

        # First 30 polls
        harris_early = sum(harris[:30]) / 30
        trump_early = sum(trump[:30]) / 30

        # Last 30 polls
        harris_late = sum(harris[-30:]) / 30
        trump_late = sum(trump[-30:]) / 30

        return harris_late - harris_early, trump_late - trump_early
        

class TestPollReader(unittest.TestCase):

    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")


def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")



if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)