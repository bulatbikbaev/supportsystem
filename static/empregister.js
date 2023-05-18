const vms = new Vue({
    delimiters: ['[[', ']]'],
    el: '#empreg',
    data: {
        username: null,
        email: null,
        last_name: null,
        first_name: null,
        middle_name: null,
        password1: null,
        password2: null,
        password_errors: null,
        success_msg: "",
        err_msg: "",
    },
    methods: {
        submitForm: function () {
            const vm = this;

            var f = document.getElementsByTagName('form')[0];

            // проверка валидности формы в html
            if (f.reportValidity() && this.password1 == this.password2) {
                f.submit();
            }
            // проверка пароля на равенство и простоту
            if (this.password1 != this.password2) {
                vm.password_errors = "Введенные пароли не совпадают"
            }

            if (this.password1.length < 6 || this.password2.length < 6) {
                vm.password_errors = "Введеный пароль слишком простой"
            }

            this.success_msg = ""
            this.err_msg = ""

            // отправка запроса
            axios({
                method: "POST",
                url: "/api/empregistration/", //django path name
                headers: {'X-CSRFTOKEN': '{{ csrf_token }}', 'Content-Type': 'application/json'},
                data: {
                    "username": this.username,
                    "email": this.email,
                    "last_name": this.last_name,
                    "first_name": this.first_name,
                    "middle_name": this.middle_name,
                    "password1": this.password1,
                    "password2": this.password2,
                },//data
            }).then(response => {
                this.success_msg = response;
            }).catch(err => {
                this.err_msg = err;
            });

        },

    },

});