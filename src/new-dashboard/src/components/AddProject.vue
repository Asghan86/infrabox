<template>
    <div>
        <md-card class="main-card">
            <md-card-header class="main-card-header">
                    <md-card-header-text>
                        <h3 class="md-title">
                            <i class="fa fa-plus-circle"></i>
                            <span> Add Project</span>
                        </h3>
                    </md-card-header-text>
            </md-card-header>
        <md-stepper>
            <md-theme md-name="running">
                <md-step :md-editable="true">
                    <h3>Select project type</h3>
                    <div class="m-t-xxl m-b-xxl">
                        <md-button-toggle md-single>
                          <md-button class="md-toggle">
                            <i class="fa fa-fw fa-upload"></i><span> Upload</span>
                          </md-button>

                          <md-button>
                            <i class="fa fa-fw fa-github"></i><span> GitHub</span>
                          </md-button>

                          <md-button>
                            <i class="fa fa-fw fa-binoculars"></i><span> Gerrit</span>
                          </md-button>
                        </md-button-toggle>
                    </div>
                </md-step>
                <md-step :md-editable="true" md-label="Project Name" :md-error="!nameValid" :md-continue="nameValid" :md-message="invalidMessage">
                    <p>Please enter your project name</p>
                    <md-input-container :class="{'md-input-invalid': !nameValid}">
                        <md-input type="text" v-model="projName" required/>
                        <label>Project Name</label>
                    </md-input-container>
                </md-step>
                <md-step>
                   <h3>Select the visibility of your project</h3>
                    <div class="m-t-xxl m-b-xxl">
                        <md-button-toggle md-single>
                          <md-button class="md-toggle">
                            <i class="fa fa-fw fa-user"></i><span> Private</span>
                          </md-button>

                          <md-button>
                            <i class="fa fa-fw fa-users"></i><span> Public</span>
                          </md-button>
                        </md-button-toggle>
                    </div>
                </md-step>
            </md-theme>
        </md-stepper>
        </md-card>
    </div>
</template>

<script>
export default {
    name: 'AddProject',
    data: () => ({
        projName: '',
        nameValid: false,
        invalidMessage: 'Name required'
    }),
    watch: {
        projName () {
            var nameRegex = /^[A-Za-z0-9]+$/

            this.nameValid = nameRegex.test(this.projName)
            console.log(this.nameValid, this.projName)
            if (this.nameValid) {
                this.invalidMessage = 'Valid name'
            } else {
                this.invalidMessage = 'Name required'
            }
        }
    }
}
</script>

<style scoped>
</style>
