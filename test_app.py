import unittest
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from parameterized import parameterized
from app import app
from solution import Solution


class TestCourseScheduleApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=cls.service)
        cls.driver.implicitly_wait(10)
        cls.client = app.test_client()  # Initialize the Flask test client

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get('http://127.0.0.1:5000/')
        self.client.post('/', data={'num_courses': '0', 'prerequisites': '[]'})

    def tearDown(self):
        self.driver.delete_all_cookies()

    @parameterized.expand([
        ("test1", '4', '[[1,0],[2,0],[3,1],[3,2]]', ['[0, 2, 1, 3]', '[0, 1, 2, 3]']),
        ("test2", '2', '[[0,1],[1,0]]', ['[]']),
        ("test3", '3', '[]', ['[0, 1, 2]', '[1, 0, 2]', '[2, 0, 1]', '[0, 2, 1]', '[1, 2, 0]', '[2, 1, 0]']),
        ("test4", '1', '[]', ['[0]']),
        ("test5", '6', '[[1,0],[2,1],[3,2],[4,3],[5,4]]', ['[0, 1, 2, 3, 4, 5]'])
    ])
    def test_course_schedule_param(self, name, num_courses, prerequisites, expected_outputs):
        num_courses_input = self.driver.find_element(By.ID, 'num_courses')
        prerequisites_input = self.driver.find_element(By.ID, 'prerequisites')

        num_courses_input.send_keys(num_courses)
        prerequisites_input.send_keys(prerequisites)
        prerequisites_input.send_keys(Keys.RETURN)

        try:
            # Use explicit wait to wait for the specific text
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, 'p'), '[')
            )
            course_order = self.driver.find_element(By.TAG_NAME, 'p').text
            self.assertIn(course_order, expected_outputs)
        except Exception as e:
            print(f"Test '{name}' failed. Page source:\n{self.driver.page_source}")
            raise e

    @patch('solution.Solution.findOrder')
    def test_mock_solution(self, mock_findOrder):
        mock_findOrder.return_value = [0, 1, 2, 3]

        # Use the Flask test client to make a POST request
        response = self.client.post('/', data={
            'num_courses': '4',
            'prerequisites': '[[1,0],[2,0],[3,1],[3,2]]'
        })

        # Verify the mock was called
        mock_findOrder.assert_called_once_with(4, [[1, 0], [2, 0], [3, 1], [3, 2]])

        # Verify the response content
        self.assertIn('[0, 1, 2, 3]', response.data.decode())

    def test_no_prerequisites(self):
        response = self.client.post('/', data={
            'num_courses': '3',
            'prerequisites': '[]'
        })
        self.assertIn('[0, 1, 2]', response.data.decode())

    def test_invalid_prerequisites_format(self):
        response = self.client.post('/', data={
            'num_courses': '3',
            'prerequisites': 'invalid_format'
        })
        self.assertIn('Invalid prerequisites format', response.data.decode())

    def test_invalid_number_format(self):
        response = self.client.post('/', data={
            'num_courses': 'invalid_number',
            'prerequisites': '[]'
        })
        self.assertIn('Invalid number format', response.data.decode())

    @patch('app.Solution')
    def test_general_exception(self, MockSolution):
        MockSolution.side_effect = Exception('General error')
        response = self.client.post('/', data={
            'num_courses': '3',
            'prerequisites': '[]'
        })
        self.assertIn('Error: General error', response.data.decode())

    def test_findOrder_no_prerequisites(self):
        self.assertEqual(Solution().findOrder(3, []), [0, 1, 2])

    def test_findOrder_with_prerequisites(self):
        result = Solution().findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
        self.assertTrue(result == [0, 2, 1, 3] or result == [0, 1, 2, 3])

    def test_findOrder_with_cycle(self):
        self.assertEqual(Solution().findOrder(2, [[0, 1], [1, 0]]), [])

    def test_findOrder_complex_dependencies(self):
        self.assertEqual(Solution().findOrder(6, [[1, 0], [2, 1], [3, 2], [4, 3], [5, 4]]), [0, 1, 2, 3, 4, 5])

    def test_findOrder_single_course(self):
        self.assertEqual(Solution().findOrder(1, []), [0])

    def test_findOrder_invalid_input(self):
        with self.assertRaises(TypeError):
            Solution().findOrder('invalid', [[1, 0]])

    def test_example_1(self):
        self.assertEqual(Solution().findOrder(2, [[1, 0]]), [0, 1])

    def test_example_2(self):
        result = Solution().findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
        self.assertTrue(result == [0, 2, 1, 3] or result == [0, 1, 2, 3])

    def test_example_3(self):
        self.assertEqual(Solution().findOrder(1, []), [0])

    def test_no_prerequisites(self):
        self.assertEqual(Solution().findOrder(3, []), [0, 1, 2])

    def test_impossible_to_complete(self):
        self.assertEqual(Solution().findOrder(2, [[0, 1], [1, 0]]), [])

    def test_large_case(self):
        numCourses = 5
        prerequisites = [[1, 0], [2, 0], [3, 1], [4, 3], [2, 4]]
        result = Solution().findOrder(numCourses, prerequisites)
        self.assertTrue(result == [] or result == [0, 1, 3, 4, 2] or result == [0, 2, 1, 3, 4])

    def test_multiple_valid_outputs(self):
        result = Solution().findOrder(3, [[0, 1], [0, 2], [1, 2]])
        self.assertTrue(result == [2, 1, 0] or result == [2, 0, 1])

    def test_no_courses(self):
        self.assertEqual(Solution().findOrder(0, []), [])

    def test_course_with_no_dependencies(self):
        self.assertEqual(Solution().findOrder(3, [[1, 0]]), [0, 1, 2])

    def test_max_constraints(self):
        numCourses = 2000
        prerequisites = [[i, i - 1] for i in range(1, numCourses)]
        result = Solution().findOrder(numCourses, prerequisites)
        self.assertTrue(self.is_valid_topological_sort(numCourses, prerequisites, result))

    def is_valid_topological_sort(self, numCourses, prerequisites, order):
        if len(order) != numCourses:
            return False
        position = {course: i for i, course in enumerate(order)}
        for crs, pre in prerequisites:
            if position[crs] <= position[pre]:
                return False
        return True

    def test_bug_report_example(self):
        numCourses = 4
        prerequisites = [[1, 0], [2, 1], [3, 2], [0, 3]]  # for creating a cycle
        self.assertEqual(Solution().findOrder(numCourses, prerequisites), [])


if __name__ == '__main__':
    unittest.main()
