var app = new Vue({
    el: '#profile',
    data: {
        confirmUser: '',
        username: document.getElementById("usernameInput").value ,
        password: '',
        reEnterPassword: '',
        error: ''
    },
    mounted() {
        getNotifications()
        window.addEventListener('keydown', function (e) {
            if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
                if (e.target.nodeName == 'INPUT' && e.target.type == 'text') {
                    e.preventDefault();
                    return false;
                }
            }
        }, true);
    },
    computed: {
        confirmDelete: function () {
            if (this.confirmUser.trim() === this.username)
                return true
            else return false
        },

        confirmDeleteFieldColor: function () {
            if (this.confirmDelete) {
                return {"border-color": "green"}
            } else {
                return {"border-color": "red"}
            }
        },


        canUpdate: function () {
            if (this.password.length > 0 && this.username && this.reEnterPassword.length > 0 && this.password === this.reEnterPassword) {
                this.error = ""
                return true
            } else {
                if (this.password) this.error = "Passwords do not match"
                return false
            }
        }


    },
    delimiters: ['[[', ']]']
})