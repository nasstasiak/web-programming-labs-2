let currentPage = 1; // Текущая страница
    const booksPerPage = 10; // Количество книг на странице
    let allBooks = []; // Массив для хранения всех книг
    let originalBooks = []; // Исходный массив книг

    // Функция для получения списка книг
    async function fetchBooks() {
        try {
            const response = await fetch('/rgz/json-rpc-api/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'get_books',
                    id: 1
                })
            });
            if (!response.ok) {
                throw new Error('Ошибка при загрузке данных');
            }
            const data = await response.json();
            if (data.result) {
                originalBooks = data.result;
                allBooks = [...originalBooks]; // Копируем исходный список
                applySorting(); // Применяем сортировку
                displayBooks(currentPage); // Отображаем книги для текущей страницы
                updatePagination(); // Обновляем пагинацию
                populateDropdowns(); // Заполняем выпадающие списки
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось загрузить список книг. Попробуйте позже.');
        }
    }

    // Функция для отображения книг на текущей странице
    function displayBooks(page) {
        const booksTable = document.getElementById('books');
        booksTable.innerHTML = '';

        // Вычисляем диапазон книг для текущей страницы
        const startIndex = (page - 1) * booksPerPage;
        const endIndex = startIndex + booksPerPage;
        const booksToDisplay = allBooks.slice(startIndex, endIndex);

        // Отображаем книги
        booksToDisplay.forEach(book => {
            const row = createBookRow(book);
            booksTable.appendChild(row);
        });

        // Обновляем текущую страницу
        currentPage = page;
    }

    // Функция для создания строки книги
    function createBookRow(book) {
        const row = document.createElement('tr');
        row.dataset.id = book.id;
        row.innerHTML = `
            <td><img src="${book.cover_image}" alt="${book.title}" width="100"></td>
            <td class="editable" data-field="title">${book.title}</td>
            <td class="editable" data-field="author">${book.author}</td>
            <td class="editable" data-field="pages">${book.pages}</td>
            <td class="editable" data-field="publisher">${book.publisher}</td>
            <td class="editable" data-field="cover_image">${book.cover_image}</td> <!-- URL обложки -->
            <td>
                <button onclick="editBook(this)">Редактировать</button>
                <button onclick="deleteBook(${book.id})">Удалить</button>
            </td>
        `;
        return row;
    }

    // Функция для редактирования книги
    function editBook(button) {
        const row = button.parentElement.parentElement;
        const editableCells = row.querySelectorAll('.editable');

        // Превращаем ячейки в поля ввода
        editableCells.forEach(cell => {
            const field = cell.dataset.field;
            const value = cell.textContent;
            cell.innerHTML = `<input type="text" value="${value}" data-field="${field}">`;
        });

        // Заменяем кнопку "Редактировать" на кнопку "Сохранить"
        button.textContent = 'Сохранить';
        button.onclick = () => saveBook(button, row.dataset.id);
    }

    // Функция для сохранения изменений книги
    async function saveBook(button, bookId) {
        const row = button.parentElement.parentElement;
        const inputs = row.querySelectorAll('input');
        const updatedBook = { id: bookId };

        // Собираем данные из полей ввода
        inputs.forEach(input => {
            const field = input.dataset.field;
            updatedBook[field] = input.value.trim(); // Убираем лишние пробелы
        });

        try {
            const response = await fetch('/rgz/json-rpc-api/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'edit_book',
                    params: updatedBook,
                    id: 1
                })
            });

            if (!response.ok) {
                throw new Error('Ошибка при сохранении изменений: ' + response.statusText);
            }

            const data = await response.json();
            if (data.result === 'success') {
                alert('Книга успешно обновлена!');
                // Обновляем только строку с измененной книгой
                updateBookRow(row, updatedBook);
            } else {
                throw new Error('Ошибка при сохранении изменений: ' + JSON.stringify(data.error));
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось сохранить изменения. Попробуйте позже.');
        }
    }

    // Функция для обновления строки с измененной книгой
    function updateBookRow(row, updatedBook) {
        row.innerHTML = `
            <td><img src="${updatedBook.cover_image}" alt="${updatedBook.title}" width="100"></td>
            <td class="editable" data-field="title">${updatedBook.title}</td>
            <td class="editable" data-field="author">${updatedBook.author}</td>
            <td class="editable" data-field="pages">${updatedBook.pages}</td>
            <td class="editable" data-field="publisher">${updatedBook.publisher}</td>
            <td class="editable" data-field="cover_image">${updatedBook.cover_image}</td> <!-- URL обложки -->
            <td>
                <button onclick="editBook(this)">Редактировать</button>
                <button onclick="deleteBook(${updatedBook.id})">Удалить</button>
            </td>
        `;
    }

    // Функция для удаления книги
    async function deleteBook(bookId) {
        try {
            const response = await fetch('/rgz/json-rpc-api/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'delete_book',
                    params: { id: bookId },
                    id: 1
                })
            });
            if (!response.ok) {
                throw new Error('Ошибка при удалении книги');
            }
            const data = await response.json();
            if (data.result === 'success') {
                fetchBooks();
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось удалить книгу. Попробуйте позже.');
        }
    }

    // Функция для обновления пагинации
    function updatePagination() {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';

        const totalPages = Math.ceil(allBooks.length / booksPerPage);

        // Кнопка "Предыдущая"
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Предыдущая';
        prevButton.disabled = currentPage === 1;
        prevButton.onclick = () => changePage(currentPage - 1);
        pagination.appendChild(prevButton);

        // Кнопки для страниц
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = i;
            pageButton.onclick = () => changePage(i);
            if (i === currentPage) {
                pageButton.classList.add('active'); // Подсвечиваем текущую страницу
            }
            pagination.appendChild(pageButton);
        }

        // Кнопка "Следующая"
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Следующая';
        nextButton.disabled = currentPage === totalPages;
        nextButton.onclick = () => changePage(currentPage + 1);
        pagination.appendChild(nextButton);
    }

    // Функция для изменения страницы
    function changePage(page) {
        if (page < 1 || page > Math.ceil(allBooks.length / booksPerPage)) {
            return; // Не позволяем уйти за пределы страниц
        }
        currentPage = page;
        displayBooks(currentPage);
        updatePagination();
    }

    // Функция для создания выпадающего списка с чекбоксами
    function createDropdown(containerId, options) {
        const container = document.getElementById(containerId);
        container.innerHTML = ''; // Очищаем контейнер

        options.forEach(option => {
            const label = document.createElement('label');
            label.style.display = 'block';
            label.innerHTML = `
                <input type="checkbox" value="${option}"> ${option}
            `;
            container.appendChild(label);
        });
    }

    // Функция для заполнения выпадающих списков авторов и издательств
    function populateDropdowns() {
        const authors = [...new Set(originalBooks.map(book => book.author))]; // Уникальные авторы
        const publishers = [...new Set(originalBooks.map(book => book.publisher))]; // Уникальные издательства

        createDropdown('filter-author-checkboxes', authors);
        createDropdown('filter-publisher-checkboxes', publishers);
    }

    // Функция для отображения/скрытия выпадающих списков
    function toggleDropdown(buttonId, dropdownId) {
        const button = document.getElementById(buttonId);
        const dropdown = document.getElementById(dropdownId);

        button.addEventListener('click', () => {
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        });
    }

    // Функция для применения фильтра по авторам
    function applyAuthorFilter() {
        const dropdown = document.getElementById('filter-author-dropdown');
        dropdown.style.display = 'none'; // Скрываем выпадающий список
        applyFilters(); // Применяем фильтры
    }

    // Функция для применения фильтра по издательствам
    function applyPublisherFilter() {
        const dropdown = document.getElementById('filter-publisher-dropdown');
        dropdown.style.display = 'none'; // Скрываем выпадающий список
        applyFilters(); // Применяем фильтры
    }

    // Применение фильтров с учетом выбранных авторов и издательств
    function applyFilters() {
        const title = document.getElementById('filter-title').value.toLowerCase();
        const selectedAuthors = getSelectedValues('filter-author-checkboxes');
        const selectedPublishers = getSelectedValues('filter-publisher-checkboxes');
        const pagesFrom = parseInt(document.getElementById('filter-pages-from').value) || 0;
        const pagesTo = parseInt(document.getElementById('filter-pages-to').value) || Infinity;

        allBooks = originalBooks.filter(book => {
            return (
                book.title.toLowerCase().includes(title) &&
                (selectedAuthors.length === 0 || selectedAuthors.includes(book.author)) &&
                (selectedPublishers.length === 0 || selectedPublishers.includes(book.publisher)) &&
                book.pages >= pagesFrom &&
                book.pages <= pagesTo
            );
        });

        applySorting();
        displayBooks(1);
        updatePagination();
    }

    // Функция для получения выбранных значений из выпадающего списка
    function getSelectedValues(containerId) {
        const container = document.getElementById(containerId);
        const checkboxes = container.querySelectorAll('input[type="checkbox"]:checked');
        return Array.from(checkboxes).map(checkbox => checkbox.value);
    }

    // Очистка фильтров
    function clearFilters() {
        document.getElementById('filter-title').value = '';
        document.getElementById('filter-pages-from').value = '';
        document.getElementById('filter-pages-to').value = '';

        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => (checkbox.checked = false));

        allBooks = [...originalBooks];
        applySorting();
        displayBooks(1);
        updatePagination();
    }

    // Функция для применения сортировки
    function applySorting() {
        const sortBy = document.getElementById('sort-by').value;
        allBooks.sort((a, b) => {
            if (sortBy === 'id') return a.id - b.id;
            if (sortBy === 'title') return a.title.localeCompare(b.title);
            if (sortBy === 'author') return a.author.localeCompare(b.author);
            if (sortBy === 'pages') return a.pages - b.pages;
            if (sortBy === 'publisher') return a.publisher.localeCompare(b.publisher);
        });

        displayBooks(currentPage);
        updatePagination();
    }

    // Обработчик формы для фильтрации
    document.getElementById('filter-form').addEventListener('submit', function (event) {
        event.preventDefault();
        applyFilters();
    });

    // Обработчик формы для добавления книги
    document.getElementById('add-book-form').addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const bookData = {
            title: formData.get('title'),
            author: formData.get('author'),
            pages: formData.get('pages'),
            publisher: formData.get('publisher'),
            cover_image: formData.get('cover_image')
        };

        try {
            const response = await fetch('/rgz/json-rpc-api/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'add_book',
                    params: bookData,
                    id: 1
                })
            });
            if (!response.ok) {
                throw new Error('Ошибка при добавлении книги');
            }
            const data = await response.json();
            if (data.result === 'success') {
                // После успешного добавления книги, обновляем список книг
                fetchBooks();
                // Переходим на последнюю страницу
                const totalPages = Math.ceil(allBooks.length / booksPerPage);
                changePage(totalPages);
                this.reset();
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось добавить книгу. Попробуйте позже.');
        }
    });

    // Инициализация выпадающих списков
    toggleDropdown('filter-author-button', 'filter-author-dropdown');
    toggleDropdown('filter-publisher-button', 'filter-publisher-dropdown');

    // Загрузка книг при загрузке страницы
    fetchBooks();