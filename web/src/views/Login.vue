<template>
  <div class="login">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <el-icon :size="32" color="#409EFF">
            <Scan />
          </el-icon>
          <span>智扫通 - 用户登录</span>
        </div>
      </template>

      <el-tabs v-model="activeTab" stretch>
        <!-- 登录 -->
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名"
                prefix-icon="User"
                size="large"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                prefix-icon="Lock"
                size="large"
                show-password
                @keyup.enter="handleLogin"
              />
            </el-form-item>

            <el-form-item>
              <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                style="width: 100%"
                :loading="loginLoading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 注册 -->
        <el-tab-pane label="注册" name="register">
          <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef">
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名"
                prefix-icon="User"
                size="large"
              />
            </el-form-item>

            <el-form-item prop="email">
              <el-input
                v-model="registerForm.email"
                type="email"
                placeholder="邮箱"
                prefix-icon="Message"
                size="large"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码"
                prefix-icon="Lock"
                size="large"
                show-password
              />
            </el-form-item>

            <el-form-item prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="确认密码"
                prefix-icon="Lock"
                size="large"
                show-password
                @keyup.enter="handleRegister"
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                style="width: 100%"
                :loading="registerLoading"
                @click="handleRegister"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const router = useRouter()

const activeTab = ref('login')
const loginLoading = ref(false)
const registerLoading = ref(false)

const loginFormRef = ref<FormInstance>()
const registerFormRef = ref<FormInstance>()

const loginForm = ref({
  username: '',
  password: '',
  remember: false
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loginRules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else if (value !== registerForm.value.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return

    loginLoading.value = true
    try {
      // TODO: 调用登录API
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      ElMessage.error('登录失败')
    } finally {
      loginLoading.value = false
    }
  })
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return

    registerLoading.value = true
    try {
      // TODO: 调用注册API
      ElMessage.success('注册成功')
      activeTab.value = 'login'
    } catch (error) {
      ElMessage.error('注册失败')
    } finally {
      registerLoading.value = false
    }
  })
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
}

.login-card {
  width: 100%;
  max-width: 450px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}
</style>
