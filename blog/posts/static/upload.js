// Обработчик формы загрузки изображения при создании и редактировании поста
window.addEventListener('DOMContentLoaded', () => {

    let form = document.querySelector('#uploadForm');
    let textArea = document.querySelector('textarea#body');
    let editions = {
        'btn-bold': [' **text**', '<strong>B</strong>'],
        'btn-italic': [' _text_', '<em>I</em>'],
        'btn-underlined': [' <u>text</u>', '<u>U</u>'],
        'btn-deleted': [' ~~text~~', '<del>Зачёркнутый</del>'],
        'btn-marked': [' <mark>text<mark>', '<mark>Выделенный</mark>'],
        'btn-small': [' <small>text<small>', '<small>Мелкий</small>'],
        'btn-code': [String.raw({raw: ' ```text```'}), '<code>Код</code>'],
        'btn-kbd': [' <kbd>terminal</kbd>', '<kbd>Терминал</kbd>'],
        'btn-link': [' [title](https://url)', '<a>Ссылка</a>'],
        'btn-quote': ['  \n> цитата  ', 'Цитата'],
        'btn-img': [' ![Alt](/url/1.png "Название")', 'Изображение'],
        'btn-table': ['  \nItem | Value | Quantity  \n——— |:——:| ——-:  \nComputer | 1600 | 3  \nPhone | 12 | 2', 'Таблица'],
        'btn-note': [' примечание[^1]  \n[^1]: Все сноски отображаются в конце страницы', 'Сноска'],
        'btn-list': ['  \n1. Первый пункт списка  \n2. Второй пункт  \n⋅⋅⋅* Немаркерованный вложенный подпункт.', 'Список'],
        'btn-line': ['  \n  ***  ', 'Линия'],
    };

    function addButtons() {
        Object.keys(editions).forEach(elem => {
            let btn = document.createElement('p');
            btn.innerHTML = `
            <button type="button" class="btn btn-outline-dark w-50" id="${elem}">${editions[elem][1]}</button>`;
            document.querySelector('#right-panel').appendChild(btn);
        });
    };

    addButtons();

    document.querySelectorAll('.btn-outline-dark').forEach(elem => {
        elem.addEventListener('click', () => {
            let btn_id = elem.getAttribute('id');
            addToText(editions[btn_id][0]);
        });
    });

    function addToText(text_or_url, title='', link=false) {
        let template;

        if (link === true) {
            text = ` [${title}](${text_or_url}) `;
        } else {
            text = text_or_url;
        };

        textArea.append(text);
    };

    function addLink(item_url, item_title) {
        let row = document.createElement('div');
        row.innerHTML = `<a href="${item_url}" target="_blank">${item_title}</a>`;
        document.querySelector('#uploadedFiles').appendChild(row);
        addToText(item_url, item_title, link=true);
    };

    async function send_request(url, data={}, headers={}) {
        const resp = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: data,
        });

        if (!resp.ok){
            throw new Error(`Could not fetch ${url}, status: ${resp.status}`);
        };

        return await resp.text();
    };

    function upload(e) {
        e.preventDefault();  // сбрасывает действие по умолчанию - перезагрузку страницы

        let filename = form.inputGroupFile02.files[0].name;
        let formData = new FormData(form);

        send_request('/upload', data=formData)
            .then(url => addLink(url, filename))
            .catch(err => console.error('No response from server'));
    };

    form.addEventListener('submit', (e) => upload(e));
});
