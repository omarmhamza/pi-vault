
var app = new Vue({
    el: '#app',
    data: {
        searchText: '',
        selected_website: '',
        selected_password: '',
        url: '',
        passwords: data

    },
    mounted() {
        getNotifications()
    },
    methods: {
        showPassword: function (event) {
            this.selected_website = this.selected_password = this.url = ""
            for (var i of this.passwords) {
                if (i["id"] === event.currentTarget.id) {
                    this.selected_password = i["raw"]
                    this.selected_website = i["website"]
                    if (i["validURL"])
                        this.url = "http://" + i["website"]
                    $('#showPasswordModel').modal('show')
                    break
                }

            }

        },
        copyPassword: function (event) {

            var clipboard = new ClipboardJS('.copyTrigger', {
                container: document.getElementById('showPasswordModel')
            });
            clipboard.on('success', function (e) {
                toastr.success('Copied to clipboard')
                e.clearSelection();
            });
            clipboard.on('error', function (e) {
                toastr.error('Failed to copy')
            });

        },

        searchPasswords: function (event) {
            var filter = this.searchText.trim().toUpperCase();
            $(".card-data").each(function () {
                if ($(this).data("string").toUpperCase().indexOf(filter) < 0) {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            })

        }
    },
    delimiters: ['[[', ']]']
})