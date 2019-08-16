<style>
  #form-files-group input[type="file"]{
    position: absolute;
    top: -500px;
  }

  #form-files-group div.file-listing{
    width: 200px;
  }

  #form-files-group span.remove-file{
    color: red;
    cursor: pointer;
    float: right;
  }
</style>

<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-12">
                <h1>Posts</h1>
                <alert :message=message v-if="showMessage"></alert>
                <hr><br><br>
                    <button type="button" class="btn btn-success btn-sm" v-b-modal.post-modal>Add Post</button>
                <br><br>
                <table class="table table-hover">
                    <thead>
                        <tr>
                        <th scope="col">Title</th>
                        <th scope="col">Content</th>
                        <th scope="col">Author</th>
                        <th scope="col">Date</th>
                        <th scope="col">Photos</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(post, index) in posts" :key="index">
                        <td>{{ post.title }}</td>
                        <td>{{ post.post_content }}</td>
                        <td>{{ post.author }}</td>
                        <td>{{ post.date }}</td>
                        <td>
                            <span v-for="(photo, index) in photos" :key="index" v-if="photo.post_id===post.id">
                                <!-- <img src="{{ photo.img }}" alt=""> -->
                                <img v-bind:src="'/images/upload/${{photo.img}}'">
                            </span><br>
                        </td>
                        <td>
                            <div class="btn-group" role="group">
                            <button type="button" class="btn btn-warning btn-sm" v-b-modal.edit-post-modal @click="editPost(post)">Update</button>
                            <button type="button" class="btn btn-danger btn-sm" @click="onDeletePost(post)">Delete</button>
                            </div>
                        </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <b-modal ref="addPostModal" id="post-modal" title="Add a new post" hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
                    <b-form-input id="form-title-input" type="text" v-model="addPostForm.title" required placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-post_content-group" label="Content:" label-for="form-content-input">
                    <b-form-input id="form-post_content-input" type="text" v-model="addPostForm.post_content" placeholder="Enter content">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
                    <b-form-input id="form-author-input" type="text" v-model="addPostForm.author" placeholder="Enter author">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-date-group" label="Date:" label-for="form-date-input">
                    <b-form-input id="form-date-input" type="date" v-model="addPostForm.date">
                    </b-form-input>
                </b-form-group>

                <b-form-group id="form-files-group" label="Files:" label-for="form-files-input">
                    <div class="large-12 medium-12 small-12 cell">
                        <input type="file" id="files" ref="files" name="files" multiple v-on:change="handleFilesUpload()"/>
                    </div>
                    <div class="large-12 medium-12 small-12 cell">
                        <div v-for="(file, key) in files" class="file-listing">{{ file.name }} <span class="remove-file" v-on:click="removeFile( key )">Remove</span></div>
                    </div>
                    <div class="large-12 medium-12 small-12 cell">
                        <button v-on:click="addFiles()">Add Files</button>
                    </div>
                </b-form-group>

                <b-button type="submit" variant="primary">Submit</b-button>
                <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>
        </b-modal>

        <b-modal ref="editPostModal" id="edit-post-modal" title="Edit post" hide-footer>
            <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
                    <b-form-input id="form-title-input" type="text" v-model="addPostForm.title" required placeholder="Enter title">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-post_content-group" label="Content:" label-for="form-content-input">
                    <b-form-input id="form-post_content-input" type="text" v-model="addPostForm.post_content" placeholder="Enter content">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-author-group" label="Author:" label-for="form-author-input">
                    <b-form-input id="form-author-input" type="text" v-model="addPostForm.author" placeholder="Enter author">
                    </b-form-input>
                </b-form-group>
                <b-form-group id="form-date-group" label="Date:" label-for="form-date-input">
                    <b-form-input id="form-date-input" type="date" v-model="addPostForm.date">
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
            posts: [],
            addPostForm: {
                title: '',
                post_content: '',
                author: '',
                date: '',
                files: [],
            },
            editForm: {
                id: '',
                title: '',
                post_content: '',
                author: '',
                date: '',
            },
            message: '',
            showMessage: false,
            files: [],
        };
    },
    components: {
        alert: Alert,
    },
    methods: {
        addFiles(){
                this.$refs.files.click();
        },
        handleFilesUpload(){
            let uploadedFiles = this.$refs.files.files;

            for( var i = 0; i < uploadedFiles.length; i++ ){
                this.files.push( uploadedFiles[i] );
            }
        },
        removeFile( key ){
            this.files.splice( key, 1 );
        },

        getPosts() {
            const path = 'http://localhost:5000/API/posts';
            axios.get(path)
                .then((res) => {
                    this.posts = res.data.posts;
                    this.photos = res.data.photos;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        addPost(payload){
            let formData = new FormData();
            formData.append('postData', JSON.stringify(payload));

            for( var i = 0; i < this.files.length; i++ ){
                let file = this.files[i];

                formData.append('files[' + i + ']', file);
                // console.log(file);
            }

            axios.post( 'http://localhost:5000/API/posts', formData, {
                headers: {
                    //'Content-Type': 'application/json'
                    'Content-Type': 'multipart/form-data'
                }
            }).then(function(){
                console.log('SUCCESS!!');
                this.getPosts();
                this.message = 'Post added!';
                this.showMessage = true;
            })
            .catch(function(){
                console.log('FAILURE!!');
                // this.getPosts();
            });
        },
        initForm(){
            this.addPostForm.title = '';
            this.addPostForm.post_content = '';
            this.addPostForm.author = '';
            this.addPostForm.date = '';

            this.editForm.title = '';
            this.editForm.post_content = '';
            this.editForm.author = '';
            this.editForm.date = '';
        },
        onSubmit(event){
            event.preventDefault();
            this.$refs.addPostModal.hide();
            
            const payload = {
                title: this.addPostForm.title,
                post_content: this.addPostForm.post_content,
                author: this.addPostForm.author,
                date: this.addPostForm.date,
            }

            this.addPost(payload);
            this.initForm();
        },
        onReset(event){
            event.preventDefault();
            this.$refs.addPostModal.hide();
            this.initForm();
        },
        editPost(post){
            this.editForm = post;
        },
        onSubmitUpdate(event){
            event.preventDefault();
            this.$refs.editPostModal.hide();

            const payload = {
                title: this.addPostForm.title,
                post_content: this.addPostForm.post_content,
                author: this.addPostForm.author,
                date: this.addPostForm.date,
            };
            this.updatePost(payload, this.editForm.id);
        },
        updatePost(payload, postID){
            const path = `http://localhost:5000/API/posts/${postID}`;
            axios.put(path, payload)
            .then(() => {
                this.getPosts();
                this.message = 'Post updated!';
                this.showMessage = true;
            })
            .catch((error) => {
                console.log(error);
                this.getPosts();
            })
        },
        onResetUpdate(event){
            event.preventDefault();
            this.$refs.editPostModal.hide();
            this.initForm();
            this.getPosts();
        },
        removePost(postID){
            const path = `http://localhost:5000/API/posts/${postID}`;
            axios.delete(path)
            .then(() => {
                this.getPosts();
                this.message = 'Post removed';
                this.showMessage = true;
            })
            .catch((error) => {
                console.log(error);
                this.getPosts();
            });
        },
        onDeletePost(post){
            this.removePost(post.id);
        }
    },
    created() {
        this.getPosts();
    },
};
</script>