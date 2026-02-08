from main import BooksCollector
import pytest

class TestBooksCollector:

    @pytest.mark.parametrize(
            'book_name, should_be_added', 
            [
                ('Нормальная книга', True),
                ('', False),                    # пустая строка
                ('A' * 41, False),              # слишком длинная
            ]
        )
    def test_add_new_book_different_names(self, book_name, should_be_added):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) == should_be_added
    
    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_new_book('Книга')  
        assert len(collector.books_genre) == 1
    
    def test_add_new_book_initial_genre_empty(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        assert collector.books_genre['Книга'] == ''
    
    def test_set_book_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        assert collector.books_genre['Книга'] == 'Фантастика'
    
    def test_set_book_genre_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая', 'Фантастика')
        assert 'Несуществующая' not in collector.books_genre
    
    
    @pytest.mark.parametrize(
            'book_name, expected_genre', 
            [
                ('Книга с жанром', 'Фантастика'),
                ('Книга без жанра', ''),
            ]
        )
    def test_get_book_genre_different_cases(self, book_name, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        if expected_genre:
            collector.set_book_genre(book_name, expected_genre)
        assert collector.get_book_genre(book_name) == expected_genre
    
    def test_get_books_with_specific_genre_found(self):
        collector = BooksCollector()
        collector.add_new_book('Фантастика 1')
        collector.add_new_book('Фантастика 2')
        collector.add_new_book('Ужасы 1')
        collector.set_book_genre('Фантастика 1', 'Фантастика')
        collector.set_book_genre('Фантастика 2', 'Фантастика')
        collector.set_book_genre('Ужасы 1', 'Ужасы')
        
        result = collector.get_books_with_specific_genre('Фантастика')
        assert 'Фантастика 1' in result and 'Фантастика 2' in result
    
    def test_get_books_with_specific_genre_not_found(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        result = collector.get_books_with_specific_genre('Несуществующий')
        assert result == []

    
    @pytest.mark.parametrize(
            'genre, is_for_children', 
            [
                ('Фантастика', True),
                ('Ужасы', False),
                ('Детективы', False),
                ('Мультфильмы', True),
                ('Комедии', True),
            ]
        )
    def test_get_books_for_children_different_genres(self, genre, is_for_children):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)        
        result = collector.get_books_for_children()
        assert ('Книга' in result) == is_for_children

    def test_get_books_genre_returns_correct_dictionary():
        collector = BooksCollector()
        collector.add_new_book("Война и мир")
        collector.add_new_book("Преступление и наказание")
        collector.set_book_genre("Война и мир", "Фантастика")
        result = collector.get_books_genre()
        expected_result = {
        "Война и мир": "Фантастика",
        "Преступление и наказание": ""
        }
        assert result == expected_result
    

    def test_add_book_in_favorites_valid(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        assert 'Книга' in collector.favorites
    
    def test_add_book_in_favorites_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')  # дубликат
        assert collector.favorites.count('Книга') == 1
        
    def test_delete_book_from_favorites_existing(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.favorites
        
    @pytest.mark.parametrize(
            'favorite_books, expected_count', 
            [
                ([], 0),
                (['Книга1'], 1),
                (['Книга1', 'Книга2', 'Книга3'], 3),
            ]
        )
    def test_get_list_of_favorites_books_different_counts(self, favorite_books, expected_count):
        collector = BooksCollector()
        for book in favorite_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        
        result = collector.get_list_of_favorites_books()
        assert len(result) == expected_count
        
