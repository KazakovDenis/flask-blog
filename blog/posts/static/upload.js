// Обработчик формы загрузки изображения при создании и редактировании поста
window.addEventListener('DOMContentLoaded', () => {

    let form = document.querySelector('#uploadForm');

    function addItem(item_url, item_title) {
        let row = document.createElement('div');
        row.innerHTML = `<a href="${item_url}" target="_blank">${item_title}</a>`;
        document.querySelector('#uploadedFiles').appendChild(row);
    };

    function upload(e) {
        e.preventDefault();  // сбрасывает действие по умолчанию - перезагрузку страницы

        let filename = form.inputGroupFile02.files[0].name;
        let formData = new FormData(form);

        let xhr = new XMLHttpRequest();

        xhr.open('POST', '/upload');
        xhr.send(formData);
        xhr.addEventListener('load', function() {
            if (xhr.status === 200) {
                addItem(xhr.response, filename);
            } else {
                console.log(xhr.response);
            };
        });
    };
    //
    // async function async_upload(url, data={}, headers={}) {
    //     const resp = await fetch(url, {
    //         method: 'POST',
    //         headers: headers,
    //         body: data,
    //     });
    //
    //     if (!resp.ok){
    //         throw new Error(`Could not fetch ${url}, status: ${resp.status}`);
    //     };
    //
    //     return await resp.text();
    // };
    //
    // async_upload('/upload', data=formData)
    //     .then(data => addItem(data, formData.files[]))
    //     .catch(err => console.console.error());
    //

    form.addEventListener('submit', (e) => upload(e));
});
