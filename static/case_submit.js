const vms = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        title: null,
        start_job: null,
        end_job: null,
        type: null,
        theme: null,
        declaration: null,
        report: null,
        specification: null,
        sp_checkbox: null,
        success_msg: "",
        err_msg: "",
    },
    methods: {
        getDeclarationFile: function (e) {
            let file = e.target.files[0];
            this.declaration = file;
        },
        getReportFile: function (e) {
            let file = e.target.files[0];
            this.report = file;
        },
        getSpecificationFile: function (e) {
            let file = e.target.files[0];
            this.specification = file;
        },
        submitForm: function () {
            // проверка валидности токена
            axios({
                method: "POST",
                url: "/api/token/verify/", //django path name
                data: {
                    "token": localStorage.getItem('my-app-auth')
                }
            }).then(response => {
                // Если токен валидный, делаем запрос на /api/case/
                // проверка валидности формы в html
                var f = document.getElementsByTagName('form')[0];
                if (f.reportValidity()) {
                    f.submit();
                }
                this.success_msg = ""
                this.err_msg = ""
                // Добавление jwt токена в запрос
                axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('my-app-auth')}`;
                axios({
                    method: "POST",
                    url: "/api/case/", //django path name
                    headers: {'X-CSRFTOKEN': '{{ csrf_token }}', 'Content-Type': 'multipart/form-data'},
                    credentials: 'same-origin',
                    data: {
                        "type": this.type,
                        "title": this.title,
                        "theme": this.theme,
                        "start_job": this.start_job,
                        "end_job": this.end_job,
                        "declaration": this.declaration,
                        "report": this.report,
                        "specification": this.specification
                    },//data
                }).then(response => {
                    this.success_msg = response;
                    window.location.href = case_list;
                }).catch(err => {
                    this.err_msg = err;
                });
            }).catch(error => {
                // Если ошибка с кодом 401, то значит срок действия токена вышел
                if (error.response.status == '401') {
                    // Обновляем токены
                    axios({
                        method: "POST",
                        url: "/api/token/refresh/", //django path name
                        data: {
                            "refresh": localStorage.getItem('my-refresh-token')
                        }
                    }).then(response => {
                        const token = response.data.access; // получаем access токен из ответа сервера
                        const refreshToken = response.data.refresh; // получаем refresh токен из ответа сервера
                        localStorage.setItem('my-app-auth', token); // сохраняем access токен в localStorage
                        localStorage.setItem('my-refresh-token', refreshToken); // сохраняем refresh токен в localStorage

                        // Повторно вызываем метод submitForm, чтобы снова проверить валидность токена
                        this.submitForm();
                    }).catch(error => {
                    })
                }
            });
        },
    },
});