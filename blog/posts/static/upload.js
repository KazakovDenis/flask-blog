// Обработчик формы загрузки изображения при создании и редактировании поста
window.addEventListener('DOMContentLoaded', () => {

    function getFile() {
        let file = document.querySelector('#inputGroupFile02').files[0];
        return file
    };

    function req() {

        var request = new XMLHttpRequest();
        request.open('POST', '/upload');
        request.setRequestHeader('Access-Control-Allow-Origin', '*');

        file = getFile();
        console.log(file);
        request.send(file);

        request.addEventListener('load', function() {

            if (request.status === 200) {
                data = request.response;
                console.log(request.response);

                let row = document.createElement('div');
                row.innerHTML = `<p><a href="${data}">Загруженное изображение</a></p>`;
                document.querySelector('#uploadedFiles').appendChild(row);
                };
        });

        request.onload = () => alert(xhr.response);
    };

    document.querySelector('#inputGroupFileAddon02').addEventListener('submit', function (event) {
        this.addEventListener('click', req);
    },true);


});