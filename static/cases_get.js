const vms = new Vue({
    el: '#cases',
    data: {
    cases: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/cases/')
        .then(function (response) {
            console.log(response.data),
            vm.cases = response.data}
        )
    }
})
