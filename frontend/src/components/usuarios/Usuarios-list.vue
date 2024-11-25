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
        router.push('/login')
        return false
    }
}

// Función para cargar usuarios si se tienen permisos
const fetchUsuarios = async () => {
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
    router.push("/equipo-create")
}

// Función para validar si usuario ya existe por su correo
const readUserByid = async (id) => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(
            `http://127.0.0.1:5000/usuarios/${id}`,
            //{},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        const userCorreo = response.data.correo
        const userId = response.data.id
        console.log(response)
        if (response.status === 201) {
            console.log(userCorreo)
            return userCorreo
            //successMessage.value = ''
            //errorMessage.value = 'Usuario ya existe con este correo'
            return false
        } else {
            successMessage.value = ''
            errorMessage.value = ''
            return true
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al leer el usuario por correo. (catch)'
        successMessage.value = ''
    }
}

// Función para eliminar un usuario
const removeUser = async (id) => {
    if (!confirm(`Seguro que desea eliminar el usuario ID: ${id}`)) {
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

        if (response.status === 201) {
            usuarios.value = response.data
            successMessage.value = 'Usuario eliminado exitosamente.'
            errorMessage.value = ''
            fetchUsuarios()
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
    fetchUsuarios()
})
</script>

<template>
    <main class="container">
        <section class="form">
            <h1 class="form__title">Gestión de usuarios</h1>
            <nav class="form__buttonsgroup">
                <button @click="redirectCreate()" class="form__button btn btn-primary">Agregar</button>
                <button @click="goBack" class="form__button btn btn-secondary">Regresar al menú</button>
            </nav>
            <!-- Zona mensajes -->
            <div v-show="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
            </div>
            <div v-show="successMessage" class="alert alert-success" role="alert">
                {{ successMessage }}
            </div>

            <!-- Listado de usuarios -->
            <table v-if="usuarios.length > 0" class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Nombres</th>
                        <th scope="col">Correo</th>
                        <th scope="col">Perfil</th>
                        <th scope="col">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="usuario in usuarios" :key="usuario.id">
                        <td>{{ usuario.id }}</td>
                        <td>{{ usuario.nombre }}</td>
                        <td>{{ usuario.correo }}</td>
                        <td>{{ usuario.perfil }}</td>

                        <td>
                            <button @click="removeUser(usuario.id)" class="btn btn-danger"><i
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