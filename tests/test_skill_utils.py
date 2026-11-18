import unittest
from skill_utils import compare, skills_in

class SkillTests(unittest.TestCase):
    def test_match_and_gap(self):
        matched, missing, score = compare("Python, SQL", "Python, SQL, Docker")
        self.assertEqual(matched, ["python", "sql"])
        self.assertEqual(missing, ["docker"])
        self.assertAlmostEqual(score, 66.6666667)
    def test_empty_job(self):
        self.assertEqual(compare("Python", "")[2], None)
    def test_no_substring_match(self):
        self.assertNotIn("java", skills_in("javascript"))
        self.assertNotIn("git", skills_in("github"))
    def test_cpp(self):
        self.assertIn("c++", skills_in("C++ developer"))

if __name__ == "__main__":
    unittest.main()
