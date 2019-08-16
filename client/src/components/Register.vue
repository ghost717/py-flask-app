<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <form v-on:submit.prevent="register">
                    <h1 class="h3 mb-3 font-weight-normal">Register</h1>
                     <div class="form-group">
                        <label for="first_name">First name</label>
                        <input type="text" name="first_name" id="first_name" v-model="first_name" class="form-control" placeholder="Enter name">
                    </div>
                    <div class="form-group">
                        <label for="last_name">Last name</label>
                        <input type="text" name="last_name" id="last_name" v-model="last_name" class="form-control" placeholder="Enter last name">
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" name="email" id="email" v-model="email" class="form-control" placeholder="Enter email">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" name="password" id="password" v-model="password" class="form-control" placeholder="Enter password">
                    </div>
                    <button class="btn btn-lg btn-primary btn-block">Register</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import router from "../router";
// import EventBus from "./EventBus";

export default {
    data(){
        return {
            first_name: '',
            last_name: '',
            email: '',
            password: ''
        }
    },
    methods:{
        register(){
            axios.post('http://localhost:5000/API/users/register', {
                first_name: this.first_name,
                last_name: this.last_name,
                email: this.email,
                password: this.password
            }).then((res) => {
                console.log(res);
                router.push({name: 'Login'})
            }).catch((err) => {
                console.log(err);
            })
        }
    }
}
</script>
