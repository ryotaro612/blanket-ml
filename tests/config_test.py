import unittest


class TestConfig(unittest.TestCase):

    def test_config(self):
        from blanketml.config import Config

        config = Config()
        self.assertIsInstance(config, Config)

        # Test default values
        self.assertEqual(config.config_file, "config.yaml")
        self.assertEqual(config.model_name, "default_model")
        self.assertEqual(config.dataset_name, "default_dataset")
        self.assertEqual(config.output_dir, "output")
        self.assertEqual(config.batch_size, 32)
        self.assertEqual(config.learning_rate, 0.001)
