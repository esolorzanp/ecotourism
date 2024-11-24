<template>
    <main class="container">
        <form class="form" @submit.prevent="login">
            <h1 class="form__title">Login</h1>
            <div class="form-floating mb-3">
                <input type="email" v-model="email" class="form-control" id="email" placeholder="name@example.com"
                    required>
                <label for="floatingInput">Corre electrónico</label>
            </div>
            <div class="form-floating mb-3">
                <input type="password" v-model="password" class="form-control" id="password"
                    placeholder="name@example.com" required>
                <label for="floatingInput">Contraseña</label>
            </div>
            <div class="form__buttonsgroup">
                <button type="submit" class="form__button btn btn-primary" @click="showToast = false">Ingresar</button>
                <button type="" class="form__button btn btn-secondary">Limpiar</button>
            </div>
        </form>
        

        <div v-if="showToast"
            class="toast align-items-center text-white bg-danger border-0 position-fixed bottom-0 end-0 p-3"
            role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    No se pudo validar la información.
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="showToast = false"></button>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const email = ref('')
const password = ref('')
const showToast = ref(false)

const login = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            correo: email.value,
            clave: password.value
        })

        // Almacenar el token en localStorage si el inicio de sesión es exitoso
        const token = response.data.access_token
        localStorage.setItem('token', token)

        // Redirigir al menú principal
        router.push('/menu')
    } catch (error) {
        // Mostrar el toast en caso de error de autenticación
        showToast.value = true
    }
}
</script>

<style scoped>
.form {
    width: 700px;
    margin: 0 auto;
    margin-top: 90px;
}
</style>