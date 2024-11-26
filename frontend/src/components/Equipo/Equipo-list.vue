<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const equipo = ref([])
const errorMessage = ref('')
const successMessage = ref('')
let usuarioIdPerfil = ''

// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 2 & perfil !== 3) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
            router.push('/menu')
            return false
        }
        usuarioIdPerfil = perfil
        return token  // Retornamos el token si es empleado o supervisor
    } else {
        router.push('/login')
        return false
    }
}

// Función para cargar integrantes del equipo si se tienen permisos
const fetchEquipo = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get('http://127.0.0.1:5000/equipo', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            equipo.value = response.data
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar los integrantes del equipo'
        }
    }
}

const redirectCreate = () => {
    router.push("/equipo-create")
}

// Función para eliminar un integrante de equipo
const removeEquipo = async (id) => {
    if (!confirm(`Seguro que desea eliminar el integrante de equipo ID: ${id}`)) {
        return
    }

    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.delete(`http://127.0.0.1:5000/equipo/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            equipo.value = response.data
            successMessage.value = 'Integrante de equipo eliminado exitosamente.'
            errorMessage.value = ''
            fetchEquipo()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al cargar los integrantes de equipos. removeEquipo'
        successMessage.value = ''
    }

}

// Volver al menú principal
const goBack = () => {
    router.push('/menu')
}

// Cargar equipo al montar el componente
onMounted(() => {
    fetchEquipo()
})
</script>

<template>
    <main class="container">
        <section class="form">
            <h1 class="form__title">Gestión de Equipo</h1>
            <nav class="form__buttonsgroup">
                <button v-if="usuarioIdPerfil === 2" @click="redirectCreate()"
                    class="form__button btn btn-primary">Agregar</button>
                <button @click="goBack" class="form__button btn btn-secondary">Regresar al menú</button>
            </nav>
            <!-- Zona mensajes -->
            <div v-show="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
            </div>
            <div v-show="successMessage" class="alert alert-success" role="alert">
                {{ successMessage }}
            </div>

            <!-- Listado de equipo -->
            <table v-if="equipo.length > 0" class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Nombres</th>
                        <th scope="col">Cargo</th>
                        <th scope="col">Edad</th>
                        <th scope="col">Género</th>
                        <th scope="col">Hobbies</th>
                        <th scope="col">Conocimientos</th>
                        <th scope="col">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="equip in equipo" :key="equip.id">
                        <td>{{ equip.id }}</td>
                        <td>{{ equip.nombre }}</td>
                        <td>{{ equip.cargo }}</td>
                        <td>{{ equip.edad }}</td>
                        <td>{{ equip.genero }}</td>
                        <td>{{ equip.hobbies }}</td>
                        <td>{{ equip.conocimientos }}</td>

                        <td>
                            <button v-if="usuarioIdPerfil === 2" @click="removeEquipo(equip.id)" class="btn btn-danger"><i
                                    class="bi bi-trash"></i></button>
                            <router-link v-if="usuarioIdPerfil === 2" :to="{ name: 'EquipoUpdate', params: { id: equip.id } }"
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