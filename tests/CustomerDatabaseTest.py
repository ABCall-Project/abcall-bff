import unittest
from uuid import UUID, uuid4
from datetime import datetime
from app.service.CustomerDatabase import CustomerDatabase


class CustomerDatabaseTest(unittest.TestCase):
    def setUp(self):
        """
        Set up common test data.
        """
        self.id = uuid4()
        self.customer_id = uuid4()
        self.topic = "Test Topic"
        self.content = "Test Content"
        self.created_at = datetime(2024, 11, 28, 10, 0, 0)

    def test_initialization_with_created_at(self):
        """
        Test initialization when 'created_at' is provided.
        """
        # Arrange & Act
        entry = CustomerDatabase(
            id=self.id,
            customer_id=self.customer_id,
            topic=self.topic,
            content=self.content,
            created_at=self.created_at
        )

        # Assert
        self.assertEqual(entry.id, self.id)
        self.assertEqual(entry.customer_id, self.customer_id)
        self.assertEqual(entry.topic, self.topic)
        self.assertEqual(entry.content, self.content)
        self.assertEqual(entry.created_at, self.created_at)

    def test_initialization_without_created_at(self):
        """
        Test initialization when 'created_at' is not provided.
        """
        # Arrange & Act
        entry = CustomerDatabase(
            id=self.id,
            customer_id=self.customer_id,
            topic=self.topic,
            content=self.content
        )

        # Assert
        self.assertEqual(entry.id, self.id)
        self.assertEqual(entry.customer_id, self.customer_id)
        self.assertEqual(entry.topic, self.topic)
        self.assertEqual(entry.content, self.content)
        self.assertIsNotNone(entry.created_at)
        self.assertTrue(isinstance(entry.created_at, datetime))

    def test_to_dict(self):
        """
        Test the 'to_dict' method for correct dictionary representation.
        """
        # Arrange
        entry = CustomerDatabase(
            id=self.id,
            customer_id=self.customer_id,
            topic=self.topic,
            content=self.content,
            created_at=self.created_at
        )

        # Act
        result = entry.to_dict()

        # Assert
        expected = {
            'id': str(self.id),
            'customer_id': str(self.customer_id),
            'topic': self.topic,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }
        self.assertEqual(result, expected)

    def test_to_dict_without_created_at(self):
        """
        Test the 'to_dict' method when 'created_at' is not provided.
        """
        # Arrange
        entry = CustomerDatabase(
            id=self.id,
            customer_id=self.customer_id,
            topic=self.topic,
            content=self.content
        )

        # Act
        result = entry.to_dict()

        # Assert
        self.assertEqual(result['id'], str(self.id))
        self.assertEqual(result['customer_id'], str(self.customer_id))
        self.assertEqual(result['topic'], self.topic)
        self.assertEqual(result['content'], self.content)
        self.assertIsNotNone(result['created_at'])
        self.assertTrue(isinstance(datetime.fromisoformat(result['created_at']), datetime))


if __name__ == '__main__':
    unittest.main()
