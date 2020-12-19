var app = new Vue({
    el: '#login',
    data: {
        passMethod: false,
        faceMethod: false,
        username: '',
        password: '',
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
    beforeDestroy() {

    },
    methods: {
        passwordAuth: function (event) {
            this.passMethod = !this.passMethod
            history.pushState(1, 'password')
        },
        faceAuth: function (event) {
            this.faceMethod = !this.faceMethod
            history.pushState(2, 'face')
        },
        reset: function () {
            this.faceMethod = false;
            this.passMethod = false
        }

    },
    computed: {
        canSign: function (event) {
            return !(this.username.length > 0 && this.password.length > 0)
        }
    },
    delimiters: ['[[', ']]']
})