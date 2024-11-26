<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const sitios = ref([])
const errorMessage = ref('')
const successMessage = ref('')
let usuarioIdPerfil = ''

// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 2 && perfil !== 3) {
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

// Función para cargar sitios si se tienen permisos
const fetchSitios = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get('http://127.0.0.1:5000/sitios', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            sitios.value = response.data
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar los sitios'
        }
    }
}

const redirectCreate = () => {
    router.push("/sitios-create")
}

// Función para eliminar un usuario
const removeSitio = async (id) => {
    if (!confirm(`Seguro que desea eliminar el sitio ID: ${id}`)) {
        return
    }

    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.delete(`http://127.0.0.1:5000/sitios/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            sitios.value = response.data
            successMessage.value = 'Sitio eliminado exitosamente.'
            errorMessage.value = ''
            fetchSitios()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al cargar los sitios.'
        successMessage.value = ''
    }

}


// Volver al menú principal
const goBack = () => {
    router.push('/menu')
}

// Cargar sitios al montar el componente
onMounted(() => {
    fetchSitios()
})
</script>

<template>
    <main class="container">
        <section class="form">
            <h1 class="form__title">Gestión de Sitios</h1>
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

            <!-- Listado de sitios -->
            <table v-if="sitios.length > 0" class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Descripción</th>
                        <th scope="col">Detalle</th>
                        <th scope="col">URL img</th>
                        <th scope="col">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="sitio in sitios" :key="sitio.id">
                        <td>{{ sitio.id }}</td>
                        <td>{{ sitio.descripcion }}</td>
                        <td>{{ sitio.detalle }}</td>
                        <td>{{ sitio.urlimg }}</td>

                        <td>
                            <button v-if="usuarioIdPerfil === 2" @click="removeSitio(sitio.id)"
                                class="btn btn-danger"><i class="bi bi-trash"></i></button>
                            <router-link v-if="usuarioIdPerfil === 2"
                                :to="{ name: 'SitiosUpdate', params: { id: sitio.id } }" class="btn btn-warning">
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