<template>
    <md-layout md-gutter>
        <md-layout md-column md-gutter md-flex-medium="10" md-flex-large="25" md-hide-xsmall md-hide-small></md-layout>
        <md-layout md-column md-gutter md-flex-medium="80" md-flex-large="50">
            <md-card class="clean-card">
                <md-card-area>
                    <md-card-header class="text-center">
<!--                        <div class="md-title text-center"><i class="fa fa-fw fa-sign-in"></i><span> Welcome to InfraBox!</span></div>-->
                        <div class="m-xl text-center">
                            <img src="../../../static/logo_on_transparent.svg" width="50%">
                        </div>
                        <div class="md-subheading text-center">Welcome to InfraBox!</div>
                    </md-card-header>
                    <md-card-content class="m-xl">
                        <form novalidate @submit.stop.prevent="submit">
                            <md-input-container :class="{'md-input-invalid': !mailValid}">
                                <md-input type="email" v-model="mail" required/>
                                <label>E-Mail</label>
                                <span v-if="!mailValid" class="md-error">Invalid E-Mail</span>
                            </md-input-container>
                            <md-input-container md-has-password :class="{'md-input-invalid': !pwValid}">
                                <label>Password</label>
                                <md-input type="password" v-model="password" required></md-input>
                                <span v-if="!pwValid" class="md-error">Invalid Password</span>
                            </md-input-container>
                            <md-button :md-disabled="!mailValid || !pwValid" class="md-raised md-primary"><i class="fa fa-fw fa-sign-in"></i><span> Login</span></md-button>
                        </form>
                    </md-card-content>
                </md-card-area>
                <md-card-content class="m-xl">
                    <h3 class="md-subheading">Don't have an InfraBox account?</h3>
                    <div class=" m-b-md"></div>
                    <md-button md-theme="default" class="md-raised md-primary"><i class="fa fa-fw fa-github"></i><span> Login with GitHub</span></md-button>
                    <md-button disabled>or</md-button>
                    <md-button md-theme="default" class="md-raised md-primary"><i class="fa fa-fw fa-user-plus"></i><span> Signup</span></md-button>
                </md-card-content>
            </md-card>
        </md-layout>
        <md-layout md-column md-gutter md-flex-medium="10" md-flex-large="25" md-hide-xsmall md-hide-small></md-layout>
    </md-layout>
</template>

<script>
export default {
    name: 'Login',
    data: () => ({
        mail: '',
        mailValid: false,
        password: '',
        pwValid: false
    }),
    watch: {
        mail () {
            // eslint-disable-next-line
            var emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

            this.mailValid = emailRegex.test(this.mail)
        },
        password () {
            // eslint-disable-next-line
            var pwRegex = /^.{5,20}$/
            this.pwValid = pwRegex.test(this.password)
        }
    }
}
</script>

<style scoped>
</style>
