<template>
  <div class="min-h-screen flex items-center justify-center bg-[var(--theme-bg)] px-2 py-8">
    <div class="w-full max-w-md mx-auto neon-border card-cosmic shadow-xl rounded-2xl p-8 flex flex-col items-center relative">
      <router-link
        to="/dashboard"
        class="absolute left-4 top-4 text-[var(--theme-accent)] hover:text-white transition-colors"
        aria-label="Volver al dashboard"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </router-link>
      <h1 class="text-3xl font-bold cosmic-gradient-text mb-8 text-center">Perfil de Usuario</h1>
      <div v-if="loading">
        <div class="flex justify-center items-center py-12">
          <div class="animate-cosmic-spin w-12 h-12 border-2 border-cosmic-500 rounded-full border-t-transparent"></div>
        </div>
      </div>
      <div v-else>
        <form class="w-full flex flex-col gap-4" @submit.prevent="handleSubmit">
          <FormInput label="Nombre" v-model="firstName" class="input-cosmic" />
          <FormInput label="Apellido" v-model="lastName" class="input-cosmic" />
          <div>
            <label class="block mb-1 font-semibold">Correo electrónico</label>
            <input
              type="email"
              v-model="email"
              class="input-cosmic neon-border w-full"
              autocomplete="email"
            />
          </div>
          <div>
            <label for="theme-select" class="block mb-1 font-semibold">Theme galáctico</label>
            <select
              id="theme-select"
              class="input-cosmic neon-border w-full"
              v-model="selectedTheme"
              @change="onThemeChange"
            >
              <option v-for="theme in themes" :key="theme.key" :value="theme.key">
                {{ theme.label }}
              </option>
            </select>
          </div>
          <Button :disabled="loading" type="submit" class="btn-cosmic w-full mt-8">
            Guardar
          </Button>
          <transition name="fade">
            <p v-if="success" class="text-green-400 mt-4 text-center">{{ success }}</p>
          </transition>
          <p v-if="error" class="text-red-400 mt-4 text-center">{{ error }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import FormInput from '@/components/ui/FormInput.vue';
import Button from '@/components/ui/Button.vue';
import { useTheme } from '@/utils/useTheme';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const loading = ref(true);
const error = ref(null);
const success = ref('');

const firstName = ref('');
const lastName = ref('');
const email = ref('');

// Theme selector logic
const { themes, currentTheme, applyTheme } = useTheme();
const selectedTheme = ref(currentTheme.value);

const router = useRouter();

const getEmail = () => {
  return authStore.user?.email || '';
};

const fetchProfile = async () => {
  loading.value = true;
  try {
    await authStore.fetchUserProfile();
    console.log('Perfil recibido:', JSON.stringify(authStore.user, null, 2));
    if (authStore.user) {
      console.log('user:', authStore.user);
      // Si la respuesta tiene un campo "user", usar ese objeto para email y username
      if (authStore.user.user) {
        email.value = authStore.user.user.email || '';
        firstName.value = authStore.user.first_name || '';
        lastName.value = authStore.user.last_name || '';
      } else {
        firstName.value = authStore.user.first_name || '';
        lastName.value = authStore.user.last_name || '';
        email.value = authStore.user.email || getEmail();
      }
    } else {
      console.warn('user es undefined');
      email.value = getEmail();
    }
    selectedTheme.value = currentTheme.value;
  } catch (err) {
    error.value = 'No se pudo cargar el perfil';
  } finally {
    loading.value = false;
  }
};

const onThemeChange = () => {
  applyTheme(selectedTheme.value);
};

onMounted(() => {
  fetchProfile();
});

const handleSubmit = async (e) => {
  e?.preventDefault?.();
  loading.value = true;
  error.value = null;
  success.value = '';
  console.log('1. Submit iniciado');

  try {
    const data = {
      email: email.value,
      first_name: firstName.value,
      last_name: lastName.value
    };
    console.log('Payload enviado al guardar:', data);

    if (authStore.isAuthenticated && authStore.updateProfile) {
      console.log("2. Llamando a authStore.updateProfile");
      await authStore.updateProfile(data);
      await fetchProfile();
      success.value = '¡Perfil guardado exitosamente!';
    } else {
      success.value = '¡Preferencias guardadas!';
    }
  } catch (err) {
    error.value = err?.message || 'Error al actualizar el perfil';
  } finally {
    loading.value = false;
    setTimeout(() => { success.value = ''; }, 2500);
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
