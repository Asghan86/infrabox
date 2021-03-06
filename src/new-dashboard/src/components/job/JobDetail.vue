<template>
    <div v-if="data">
        <md-card class="main-card">
            <md-card-header class="main-card-header" style="padding-bottom: 10px">
            <md-card-header-text>
                <h3 class="md-title card-title">
                <router-link :to="{name: 'ProjectDetail', params: {
                projectName: data.project.name
                }}">
                    <span v-if="data.project.isGit()"><i class="fa fa-github"></i></span>
                    <span v-if="!data.project.isGit()"><i class="fa fa-home"></i></span>
                    {{ data.project.name }}
                </router-link>
                / <router-link :to="{name: 'BuildDetail', params: {
                    projectName: data.project.name,
                    buildNumber: data.build.number,
                    buildRestartCounter: data.build.restartCounter
                    }}">
                    Build {{ data.build.number }}.{{ data.build.restartCounter }}
                </router-link>
                / <!--<router-link :to="{name: 'JobDetail', params: {
                projectName: data.project.name,
                buildNumber: data.build.number,
                buildRestartCounter: data.build.restartCounter,
                jobId: data.job.id
                }}">
                Job
                </router-link>-->
                {{ data.job.name}}
                </h3>
            </md-card-header-text>
            <md-toolbar class="md-transparent">
                <md-button class="md-icon-button" v-on:click="data.job.abort()"><md-icon>not_interested</md-icon><md-tooltip md-direction="bottom">Stop Job</md-tooltip></md-button>
                <md-button class="md-icon-button" v-on:click="data.job.restart()"><md-icon>replay</md-icon><md-tooltip md-direction="bottom">Restart Job</md-tooltip></md-button>
                <md-button class="md-icon-button" v-on:click="data.job.clearCache()"><md-icon>delete_sweep</md-icon><md-tooltip md-direction="bottom">Clear Cache</md-tooltip></md-button>
            </md-toolbar>
            </md-card-header>
            <md-card-content>
                <md-layout>
                    <md-layout md-flex-xsmall="100" md-flex-small="100" md-flex-medium="100" md-flex-large="75">
                        <md-tabs md-fixed class="md-transparent">
                            <md-tab id="console" md-label="Console" class="widget-container">
                                <ib-console></ib-console>
                            </md-tab>
                            <md-tab id="test-list" md-label="Tests">
                                tests
                            </md-tab>
                            <md-tab id="stat-list" md-label="Stats">
                                tests
                            </md-tab>
                            <md-tab id="downloads" md-label="Downloads">
                                downloads
                            </md-tab>
                        </md-tabs>
                    </md-layout>
                    <md-layout md-flex-xsmall="100" md-flex-small="100" md-flex-medium="100" md-flex-large="25">
                        <md-list class="md-dense widget-container" style="margin: 16px">
                            <ib-state-big :state="data.job.state"></ib-state-big>
                            <md-list-item class="p-l-md p-r-md p-t-md">
                                <span class="md-body-2"><i class="fa fa-calendar fa-fw p-r-xl" aria-hidden="true"></i>
                                Started</span>
                                <span class="md-list-action">
                                    <ib-date :date="data.job.startDate"></ib-date>
                                </span>
                            </md-list-item>
                            <md-list-item class="p-l-md p-r-md">
                                <span class="md-body-2"><i class="fa fa-clock-o fa-fw p-r-xl" aria-hidden="true"></i>
                                Duration</span>
                                <span class="md-list-action">
                                    <ib-duration :start="data.job.startDate" :end="data.job.endDate">
                                  </ib-duration>
                                </span>
                            </md-list-item>
                            <md-list-item class="p-l-md p-r-md">
                                <span class="md-body-2"><i class="fa fa-list-ol fa-fw p-r-xl" aria-hidden="true"></i>
                                Commit</span>
                                <span class="md-list-action">
                                    <ib-commit-sha :sha="data.build.commit.id"></ib-commit-sha>
                                </span>
                            </md-list-item>
                            <md-list-item class="p-l-md p-r-md">
                                <span class="md-body-2"><i class="fa fa-user fa-fw p-r-xl" aria-hidden="true"></i>
                                Author</span>
                                <span class="md-list-action">
                                    {{ data.build.commit.author_name }}
                                </span>
                            </md-list-item>
                            <md-list-item class="p-l-md p-r-md">
                                <span class="md-body-2"><i class="fa fa-code-fork fa-fw p-r-xl" aria-hidden="true"></i>
                                Branch</span>
                                <span class="md-list-action">
                                    {{ data.build.commit.branch }}
                                </span>
                            </md-list-item>

                        </md-list>

                    </md-layout>
                </md-layout>

            </md-card-content>
		</md-card>
    </div>
</template>

<script>
import ProjectService from '../../services/ProjectService'
import StateBig from '../utils/StateBig'
import CommitSha from '../utils/CommitSha'
import Date from '../utils/Date'
import Duration from '../utils/Duration'
import Console from './Console'

export default {
    name: 'JobDetail',
    props: ['jobId', 'projectName', 'buildNumber', 'buildRestartCounter'],
    components: {
        'ib-state-big': StateBig,
        'ib-commit-sha': CommitSha,
        'ib-date': Date,
        'ib-duration': Duration,
        'ib-console': Console
    },
    asyncComputed: {
        data: {
            get () {
                let job = null
                let build = null
                let project = null
                return ProjectService
                    .findProjectByName(this.projectName)
                    .then((p) => {
                        project = p
                        return p.getBuild(this.buildNumber, this.buildRestartCounter)
                    })
                    .then((b) => {
                        build = b
                        return build.getJob(this.jobId)
                    })
                    .then((j) => {
                        job = j
                        return {
                            project,
                            build,
                            job
                        }
                    })
            },
            watch () {
                // eslint-disable-next-line no-unused-expressions
                this.projectName
                // eslint-disable-next-line no-unused-expressions
                this.buildNumber
                // eslint-disable-next-line no-unused-expressions
                this.buildRestartCounter
                // eslint-disable-next-line no-unused-expressions
                this.jobId
            }
        }
    }
}
</script>

<style scoped>
    .widget-container {
        width: 98%;
    }
</style>

