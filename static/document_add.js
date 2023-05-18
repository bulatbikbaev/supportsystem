const vms = new Vue({
    delimiters: ['[[', ']]'],
    el: '#doc_add',
    data: {
        document_type: null,
        new_document: null,
    },
    methods: {
        getNewFile: function (e) {
            let file = e.target.files[0];
            this.new_document = file;
        },
        submitForm: function () {
                var f = document.getElementsByTagName('form')[0];
                if (f.reportValidity()) {
                    f.submit();
                }
                axios({
                    method: "POST",
                    url: "/api/case/documents/" + case_number + "/", //django path name
                    headers: {'X-CSRFTOKEN': '{{ csrf_token }}', 'Content-Type': 'multipart/form-data'},
                    credentials: 'same-origin',
                    data: {
                        "document_type": this.document_type,
                        "new_document": this.new_document,
                    },//data
                }).then(response => {
                    this.success_msg = response;
                }).catch(err => {
                    this.err_msg = err;
                });
            }
        }
});