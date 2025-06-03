<template>
  <div>
    <h1>Perfil de Usuario</h1>
    <div v-if="user">
      <FormInput label="Nombre" v-model="firstName" />
      <FormInput label="Apellido" v-model="lastName" />
      <FormInput label="Correo electrónico" v-model="email" type="email" />
      <Button :disabled="loading" @click="handleSubmit">
        Guardar
      </Button>
      <p v-if="error" style="color: red">{{ error }}</p>
    </div>
    <div v-else>
      <p>Cargando información del usuario...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import FormInput from '@/components/ui/FormInput.vue';
import Button from '@/components/ui/Button.vue';

const authStore = useAuthStore();
const user = ref(authStore.userProfile);
const loading = ref(false);
const error = ref(null);

const firstName = ref('');
const lastName = ref('');
const email = ref('');

onMounted(() => {
  if (authStore.userProfile.value) {
    firstName.value = authStore.userProfile.value.first_name || '';
    lastName.value = authStore.userProfile.value.last_name || '';
    email.value = authStore.userProfile.value.email || '';
  }
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = null;

  try {
    const data = {};
    if (firstName.value !== authStore.userProfile.value?.first_name) {
      data.first_name = firstName.value;
    }
    if (lastName.value !== authStore.userProfile.value?.last_name) {
      data.last_name = lastName.value;
    }
    if (email.value !== authStore.userProfile.value?.email) {
      data.email = email.value;
    }

    if (Object.keys(data).length > 0) {
      await authStore.updateProfile(data);
      // Actualizar la referencia local del usuario después de la actualización
      await authStore.fetchUserProfile();
      firstName.value = authStore.userProfile.value.first_name || '';
      lastName.value = authStore.userProfile.value.last_name || '';
      email.value = authStore.userProfile.value.email || '';
    }

  } catch (err) {
    error.value = err.message || 'Error al actualizar el perfil';
  } finally {
    loading.value = false;
  }
};
</script>
