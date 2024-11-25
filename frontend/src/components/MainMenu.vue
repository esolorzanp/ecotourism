<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from "jwt-decode";

const router = useRouter()
const perfil = ref(0)

onMounted(() => {
    const token = localStorage.getItem('token');

    if (token) {
        //const decodedToken = jwt_decode(token)
        const decodedToken = jwtDecode(token)
        perfil.value = decodedToken.sub.perfil_id
    } else {
        // Si no hay token, redirigir al login
        router.push('/login')
    }
})

// Función de logout que limpia el localStorage y redirige al login
const logout = () => {
    localStorage.clear()
    router.push('/login')
}
</script>

<template>
    <div class="container">
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">EcoTourism</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li v-show="perfil === 1" class="nav-item">
                            <a class="nav-link" href="/usuarios-list">Usuarios</a>
                        </li>
                        <li v-show="perfil === 2 | perfil === 3" class="nav-item">
                            <a class="nav-link" href="/sitios-list">Sitios</a>
                        </li>
                        <li v-show="perfil === 2 | perfil === 3" class="nav-item">
                            <a class="nav-link" href="/equipo-list">Equipo</a>
                        </li>
                        <li v-show="perfil === 2 | perfil === 3" class="nav-item">
                            <a class="nav-link" href="/comentarios-list">Comentarios</a>
                        </li>
                        <li v-show="perfil === 2 | perfil === 3" class="nav-item">
                            <a class="nav-link" href="/preguntasfrecuentes-list">Preguntas frecuentes</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>

</template>

<style scoped></style>