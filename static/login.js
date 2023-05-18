const vms = new Vue({
    delimiters: ['[[', ']]'],
    el: '#login',
    data: {
        username: null,
        password: null,
        login_error: null,
        success_msg: "",
        err_msg: "",
    },
    methods: {
        submitForm: function () {
            const vm = this;

            var f = document.getElementsByTagName('form')[0];
            this.success_msg = ""
            this.err_msg = ""
            axios({
                method: "POST",
                url: "/api/login/", //django path name
                headers: {'X-CSRFTOKEN': '{{ csrf_token }}', 'Content-Type': 'application/json'},
                data: {
                    "username": this.username,
                    "password": this.password
                },//data
            }).then(response => {
                this.success_msg = response.data;
                vm.login_error = response.data.access

                const token = response.data.access; // получаем access токен из ответа сервера
                const refreshToken = response.data.refresh; // получаем refresh токен из ответа сервера
                localStorage.setItem('my-app-auth', token); // сохраняем access токен в localStorage
                localStorage.setItem('my-refresh-token', refreshToken); // сохраняем refresh токен в localStorage

                // Редирект после успешного входа на главную страницу
                window.location.href = home_url
            }).catch(error => {
                vm.login_error = error.response
                if (error.response.status == '400') {
                    this.login_error = "Такого пользователя не существует";
                }
            });

        },

    },

});