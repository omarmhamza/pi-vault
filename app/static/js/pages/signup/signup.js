var app = new Vue({
    el: '#signup',
    data: {
        passMethod: false,
        faceMethod: false,
        username: '',
        password: '',
        reEnteredPassword: '',
        lastState: 0

    },
    mounted() {
        getNotifications()
        window.onpopstate = function (event) {
            if (event.state === 1 || event.state === 2) {
                this.reset()
                this.lastState = event.state
            }
        }.bind(this);

    },

    methods: {
        passwordAuth: function () {
            this.passMethod = !this.passMethod
            history.pushState(1, 'password')
        },
        faceAuth: function () {
            this.faceMethod = !this.faceMethod
            history.pushState(2, 'face')
        },
        reset: function () {
            this.faceMethod = false;
            this.passMethod = false
        }
    },
    computed: {
        canSign: function () {
            return !(this.username.length > 0 && this.password.length > 0 && this.password === this.reEnteredPassword)
        },
        checkReEnterPasswordField: function () {
            if (this.password.length > 0 && this.password === this.reEnteredPassword) {
                return {"borderColor": "green"}
            } else if (this.password.length == 0)
                return {}
            else {
                return {"borderColor": "red"}
            }
        }
    },
    delimiters: ['[[', ']]']
})