<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const perfiles = ref([])
const errorMessage = ref('')
const successMessage = ref('')

// Variables de captura
const inId = route.params.id
const inDescripcion = ref('')
const inDetalle= ref('')


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
        return token  // Retornamos el token si es empleado o supervisor
    } else {
        router.push('/login')
        return false
    }
}

// Función para cargar un usuario si se tienen permisos
const fetchSitio = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(`http://127.0.0.1:5000/sitios/${inId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
        
        if (response.status === 201) {
            const sitio = response.data
            inDescripcion.value = sitio.descripcion
            inDetalle.value = sitio.detalle
            successMessage.value = ''
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar los sitios.'
        }
    }
}


// Función para actuzalizar sitio
const updateSitio = async () => {
    const token = checkPermissions()
    if (!token) return
    //if (!camposValidos()) return
    if (!readsitioDescripcion()) return

    try {
        const response = await axios.put(
            `http://127.0.0.1:5000/sitios/${inId}`,
            {
                "descripcion": inDescripcion.value,
                "detalle": inDetalle.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201) {
            successMessage.value = 'Sitio actuzalizado  exitosamente.'
            errorMessage.value = ''
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al actualizar el sitio'
        successMessage.value = ''
    }
}

// Función para validar sitio que no exista con la misma descripción
const readsitioDescripcion = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(
            `http://127.0.0.1:5000/sitios/${inDescripcion.value}`,
            //{},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201 && response.data.length > 0) {
            successMessage.value = ''
            errorMessage.value = 'El sitio ya existe con esta descripción'
            return false
        } else {
            successMessage.value = ''
            errorMessage.value = ''
            return true
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al leer el sitio por descripción'
        successMessage.value = ''
    }
}

const camposValidos = () => {
    /*if (inClave.value != inClaveConfirmada.value) {
        errorMessage.value = 'La constraseña y su confirmación no son las mismas'
        successMessage.value = ''
        return false
    }*/
    return true
}

const limpiar = () => {
    inDescripcion.value = ''
    inDetalle.value = ''
}
// Volver al menú principal
const goBack = () => {
    router.push('/sitios-list')
}

// Verificar permisos al montar el componente
onMounted(() => {
    //checkPermissions()
    fetchSitio()
})
</script>

<template>
    <main class="container">
        <form class="form" @submit.prevent="updateSitio">
            <h1 class="form__title">Actualización de un Sitio</h1>
            <section>
                <p v-show="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
                <p v-show="successMessage" class="alert alert-success">{{ successMessage }}</p>
                <div class="form-floating mb-3">
                    <input v-model="inDescripcion" type="text" class="form-control" id="floatingDescripcion"
                        placeholder="Ingrese la descripcion" :required="true">
                    <label for="floatingDescripcion">Descripcion</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inDetalle" type="text" class="form-control" id="floatingDetalle"
                        placeholder="Ingrese la descripción" :required="true">
                    <label for="floatingDetalle">Detalle</label>
                </div>
               
                <!-- Buttons group-->
                <div class="form__buttonsgroup">
                    <button type="submit" class="form__button btn btn-primary">Actualizar</button>
                    <button @click="limpiar" class="form__button btn btn-secondary">Limpiar</button>
                    <button @click="goBack" class="form__button btn btn-secondary">Regresar al menú</button>
                </div>
            </section>
        </form>
    </main>

</template>

<style scoped>
</style>