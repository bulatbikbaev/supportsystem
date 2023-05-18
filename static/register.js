const vms = new Vue({
    delimiters: ['[[', ']]'],
    el: '#reg',
    data: {
        username: null,
        email: null,
        kpp: null,
        title: null,
        password1: null,
        password2: null,
        success_msg: "",
        err_msg: "",
    },
    methods: {
        submitForm: function () {
            var f = document.getElementsByTagName('form')[0];
            // проверка валидности формы в html
            if (f.reportValidity() && this.password1 == this.password2) {
                f.submit();
            }
            const vm = this;

            // проверка пароля на равенство и простоту
            if (this.password1 != this.password2) {
                vm.password_errors = "Введенные пароли не совпадают"
            }

            if (this.password1.length < 6 || this.password2.length < 6) {
                vm.password_errors = "Введеный пароль слишком простой"
            }

            this.success_msg = ""
            this.err_msg = ""
            axios({
                method: "POST",
                url: "/api/registration/", //django path name
                headers: {'X-CSRFTOKEN': '{{ csrf_token }}', 'Content-Type': 'application/json'},
                data: {
                    "username": this.username,
                    "email": this.email,
                    "kpp": this.kpp,
                    "title": this.title,
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