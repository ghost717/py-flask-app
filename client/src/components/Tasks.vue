<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-12">
                <h1>Tasks</h1>
                <alert :message=message v-if="showMessage"></alert>
                <hr><br><br>
                    <button type="button" class="btn btn-success btn-sm" v-b-modal.task-modal>Add Task</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Id</th>
                            <th scope="col">Title</th>
                            <th scope="col">Content</th>
                            <th scope="col">Author</th>
                            <th scope="col">Status</th>
                            <th scope="col">Date</th>
                            <th scope="col">Created</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(task, index) in tasks" :key="index">
                            <td>{{ task.id }}</td>
                            <td>{{ task.title }}</td>
                            <td>{{ task.content }}</td>
                            <td>{{ task.author }}</td>
                            <td>{{ task.status }}</td>
                            <td>{{ task.date }}</td>
                            <td>{{ task.created }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                <button type="button" class="btn btn-warning btn-sm" v-b-modal.edit-task-modal @click="editTask(task)">Update</button>
                                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteTask(task)">Delete</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <b-modal ref="addTaskModal" id="task-modal" title="Add a new task" hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
                    <b-form-input id="form-title-input" type="text" v-model="addTaskForm.title" required placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-content-group" label="Content:" label-for="form-content-input">
                    <b-form-input id="form-content-input" type="text" v-model="addTaskForm.content" placeholder="Enter content">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-status-group" label="status:" label-for="form-status-input">
                    <b-form-input id="form-status-input" type="text" v-model="addTaskForm.status" placeholder="Enter status">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
                    <b-form-input id="form-author-input" type="number" v-model="addTaskForm.author" placeholder="Enter author">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-date-group" label="Date:" label-for="form-date-input">
                    <b-form-input id="form-date-input" type="date" v-model="addTaskForm.date">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-created-group" label="Created:" label-for="form-created-input">
                    <b-form-input id="form-created-input" type="date" v-model="addTaskForm.created">
                    </b-form-input>
                </b-form-group>

                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>

        <b-modal ref="editTaskModal" id="edit-task-modal" title="Edit task" hide-footer>
            <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
                    <b-form-input id="form-title-input" type="text" v-model="addTaskForm.title" required placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-content-group" label="Content:" label-for="form-content-input">
                    <b-form-input id="form-content-input" type="text" v-model="addTaskForm.content" placeholder="Enter content">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-status-group" label="status:" label-for="form-status-input">
                    <b-form-input id="form-status-input" type="text" v-model="addTaskForm.status" placeholder="Enter status">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
                    <b-form-input id="form-author-input" type="text" v-model="addTaskForm.author" placeholder="Enter author">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-date-group" label="Date:" label-for="form-date-input">
                    <b-form-input id="form-date-input" type="date" v-model="addTaskForm.date">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-created-group" label="created:" label-for="form-created-input">
                    <b-form-input id="form-created-input" type="date" v-model="addTaskForm.created">
                    </b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Update</b-button>
                <b-button type="reset" variant="danger">Cancel</b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
    data() {
        return {
            showMessage: false,
            tasks: [],
            addTaskForm: {
                title: '',
                content: '',
                status: '',
                author: '',
                date: '',
                created: '',
            },
        }
    },
    components: {
        alert: Alert,
    },
    methods: {
        getTasks() {
            const path = 'http://localhost:5000/API/tasks';
            axios.get(path)
            .then((res) => {
                this.tasks = res.data.tasks;
                console.log(this.tasks);
            })
            .catch((error) => {
                console.error(error);
            });
        },
        addTask(payload){
            const path = 'http://localhost:5000/API/tasks';
            axios.post( path, payload, {
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(() => {
                this.getTasks();
                this.message = 'Task added!';
                this.showMessage = true;
            })
            .catch((error) => {
                console.log(error);
                this.getTasks();
            });
        },
        initForm(){
            this.addTaskForm.title = '';
            this.addTaskForm.content = '';
            this.addTaskForm.author = '';
            this.addTaskForm.status = '';
            this.addTaskForm.date = '';
            this.addTaskForm.created = '';
        },
        onSubmit(event){
            event.preventDefault();
            this.$refs.addTaskModal.hide();

            const payload = {
                title: this.addTaskForm.title,
                content: this.addTaskForm.content,
                status: this.addTaskForm.status,
                author: this.addTaskForm.author,
                date: this.addTaskForm.date,
                created: this.addTaskForm.created,
            }

            this.addTask(payload);
            this.initForm();
        },
        onReset(event){
            event.preventDefault();
            this.$refs.addTaskModal.hide();
            this.initForm();
        },
        editTask(task){
            this.editForm = task;
        },
        onSubmitUpdate(event){
            event.preventDefault();
            this.$refs.editTaskModal.hide();

            const payload = {
                title: this.addTaskForm.title,
                content: this.addTaskForm.content,
                status: this.addTaskForm.status,
                author: this.addTaskForm.author,
                date: this.addTaskForm.date,
                created: this.addTaskForm.created
            };
            this.updateTask(payload, this.editForm.id);
        },
        updateTask(payload, taskID){
            const path = `http://localhost:5000/API/tasks/${taskID}`;
            axios.put(path, payload)
            .then(() => {
                this.getTasks();
                this.message = 'Task updated!';
                this.showMessage = true;
            })
            .catch((error) => {
                console.log(error);
                this.getTasks();
            })
        },
        onResetUpdate(event){
            event.preventDefault();
            this.$refs.editTaskModal.hide();
            this.initForm();
            this.getTasks();
        },
        removeTask(taskID){
            const path = `http://localhost:5000/API/tasks/${taskID}`;
            axios.delete(path)
            .then(() => {
                this.getTasks();
                this.message = 'Task removed';
                this.showMessage = true;
            })
            .catch((error) => {
                console.log(error);
                this.getTasks();
            });
        },
        onDeleteTask(task){
            this.removeTask(task.id);
        }
    },
    created() {
        this.getTasks();
    },
}
</script>
