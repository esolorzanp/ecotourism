<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const usuarios = ref([])
const errorMessage = ref('')
const successMessage = ref('')

// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 1) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
            router.push('/menu')
            return false
        }
        return token  // Retornamos el token si es administrador
    } else {
        router.push('/menu')
        return false
    }
}

// Función para cargar usuarios si se tienen permisos
const loadUsuarios = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get('http://127.0.0.1:5000/usuarios', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            usuarios.value = response.data
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar los usuarios.'
        }
    }
}

const redirectCreate = () => {
    router.push("/usuarios-create")
}

// Función para eliminar un usuario
const remove = async (id) => {

    if (!confirm(`Seguro que desea eliminar el usuario ${correo}`)) {
        return
    }

    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.delete(`http://127.0.0.1:5000/usuarios/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 200) {
            usuarios.value = response.data
            successMessage.value = 'Usuario eliminado exitosamente.'
            errorMessage.value = ''
            loadUsuarios()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al cargar los usuarios.'
        successMessage.value = ''
    }

}

// Volver al menú principal
const goBack = () => {
    router.push('/menu')
}

// Cargar usuarios al montar el componente
onMounted(() => {
    loadUsuarios()
})
</script>

<template>
    <main class="container">
        <section class="form">
            <h1 class="form__title">Gestión de usuarios</h1>
            <nav class="form__buttonsgroup">
                <button @click="redirectCreate()" class="form__button btn btn-primary">Agregar</button>
                <button @click="goBack" class="form__button btn btn-secondary">Menú</button>
            </nav>


            <div v-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
            </div>

            <div v-if="successMessage" class="alert alert-success" role="alert">
                {{ successMessage }}
            </div>

            <table v-if="usuarios.length > 0" class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Nombres</th>
                        <th scope="col">Correo</th>
                        <th scope="col">Perfil</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="usuario in usuarios" :key="usuario.id">
                        <td>{{ usuario.nombre }}</td>
                        <td>{{ usuario.correo }}</td>
                        <td>{{ usuario.perfil }}</td>

                        <td>
                            <button @click="remove(usuario.id)" class="btn btn-danger"><i
                                    class="bi bi-trash"></i></button>
                            <router-link :to="{ name: 'UsuariosUpdate', params: { id: usuario.id } }"
                                class="btn btn-warning">
                                <i class="bi bi-pencil"></i>
                            </router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
        </section>
    </main>

</template>

<style scoped></style>