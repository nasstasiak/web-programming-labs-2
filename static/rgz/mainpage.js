let currentPage = 1; // Текущая страница
    const booksPerPage = 20; // Количество книг на странице
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
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><img src="${book.cover_image}" alt="${book.title}" width="100"></td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.pages}</td>
                <td>${book.publisher}</td>
            `;
            booksTable.appendChild(row);
        });

        // Обновляем текущую страницу
        currentPage = page;
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

    // Инициализация выпадающих списков
    toggleDropdown('filter-author-button', 'filter-author-dropdown');
    toggleDropdown('filter-publisher-button', 'filter-publisher-dropdown');

    // Загрузка книг при загрузке страницы
    fetchBooks();