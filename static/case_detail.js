new Vue({
    delimiters: ["[[", "]]"],
    el: '#case_detail',
    data: {
        case_detail: null,
        case_docs: null
    },
    created: function () {
        const vm = this;
        console.log('ID дела')
        console.log(case_number)

        // параллельные HTTP-запросы
        axios.all([
            // Данные о деле
            axios.get('/api/case/' + case_number),
            // Данные о документах
            axios.get('/api/case/documents/' + case_number)
        ])
            .then(axios.spread((case_detail, case_docs) => {
                vm.case_detail = case_detail.data
                vm.case_docs = case_docs.data.documents
                console.log('документы')
                console.log(vm.case_docs.documents)
            }))
    }
})
