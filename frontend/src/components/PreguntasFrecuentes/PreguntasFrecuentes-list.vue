<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const preguntasfrecuentes = ref([])
const errorMessage = ref('')
const successMessage = ref('')

// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 2) {
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

// Función para cargar preguntas frecuentes si se tienen permisos
const fetchPreguntasFrecuentes = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get('http://127.0.0.1:5000/preguntasfrecuentes', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
        if (response.status === 201) {
            preguntasfrecuentes.value = response.data
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar las preguntas frecuentes.'
        }
    }
}

const redirectCreate = () => {
    router.push("/preguntasfrecuentes-create")
}

// Función para eliminar una pregunta frecuente
const removePreguntasFrecuentes = async (id) => {
    if (!confirm(`Seguro que desea eliminar la pregunta frecuente ID: ${id}`)) {
        return
    }

    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.delete(`http://127.0.0.1:5000/preguntasfrecuentes/${id}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            preguntasfrecuentes.value = response.data
            successMessage.value = 'Pregunta frecuente eliminada exitosamente.'
            errorMessage.value = ''
            fetchPreguntasFrecuentes()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al eliminar la pregunta frecuente'
        successMessage.value = ''
    }

}

// Volver al menú principal
const goBack = () => {
    router.push('/menu')
}

// Cargar usuarios al montar el componente
onMounted(() => {
    fetchPreguntasFrecuentes()
})
</script>

<template>
    <main class="container">
        <section class="form">
            <h1 class="form__title">Gestión de preguntas frecuentes</h1>
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

            <!-- Listado de Preguntas Frecuentes -->
            <table v-if="preguntasfrecuentes.length > 0" class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Pregunta</th>
                        <th scope="col">Respuesta</th>
                        <th scope="col">Orden</th>
                        <th scope="col">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="preguntafrecuente in preguntasfrecuentes" :key="preguntafrecuente.id">
                        <td>{{ preguntafrecuente.id }}</td>
                        <td>{{ preguntafrecuente.pregunta }}</td>
                        <td>{{ preguntafrecuente.respuesta }}</td>
                        <td>{{ preguntafrecuente.orden }}</td>

                        <td>
                            <button @click="removePreguntasFrecuentes(preguntafrecuente.id)" class="btn btn-danger"><i
                                    class="bi bi-trash"></i></button>
                            <router-link :to="{ name: 'PreguntasFrecuentesUpdate', params: { id: preguntafrecuente.id } }"
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