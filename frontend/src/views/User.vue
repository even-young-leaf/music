<template>
  <div class="user-page">
    <div class="user-header">
      <div class="user-avatar">
        <img :src="user.avatar || '/static/image/default_avatar.jpg'" alt="头像">
      </div>
      
      <div class="user-info">
        <h1>{{ user.username || '用户' }}</h1>
        <p class="user-id">用户ID: {{ user.id }}</p>
        <p class="join-date">注册时间: {{ user.join_date }}</p>
        <p class="email">邮箱: {{ user.email }}</p>
      </div>
    </div>
    
    <div class="user-tabs">
      <div class="tab" 
           v-for="(tab, index) in tabs" 
           :key="index"
           :class="{ active: activeTab === index }"
           @click="activeTab = index">
        {{ tab.name }}
      </div>
    </div>
    
    <div class="tab-content">
      <!-- 收藏的歌曲 -->
      <div v-if="activeTab === 0" class="favorite-songs">
        <h2>我的收藏</h2>
        
        <table v-if="favoriteSongs.length > 0">
          <thead>
            <tr>
              <th>歌曲</th>
              <th>歌手</th>
              <th>专辑</th>
              <th>收藏时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="song in favoriteSongs" :key="song.id">
              <td>
                <router-link :to="`/play/${song.id}`">{{ song.name }}</router-link>
              </td>
              <td>{{ song.singer }}</td>
              <td>{{ song.album }}</td>
              <td>{{ song.favorite_time }}</td>
              <td>
                <button class="action-btn play" @click="playSong(song)">
                  播放
                </button>
                <button class="action-btn remove" @click="removeFavorite(song.id)">
                  取消收藏
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div class="empty-list" v-else>
          <p>暂无收藏歌曲</p>
        </div>
      </div>
      
      <!-- 最近播放 -->
      <div v-if="activeTab === 1" class="recent-plays">
        <h2>最近播放</h2>
        
        <table v-if="recentPlays.length > 0">
          <thead>
            <tr>
              <th>歌曲</th>
              <th>歌手</th>
              <th>播放时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="play in recentPlays" :key="play.id">
              <td>
                <router-link :to="`/play/${play.song_id}`">{{ play.song_name }}</router-link>
              </td>
              <td>{{ play.singer }}</td>
              <td>{{ play.play_time }}</td>
              <td>
                <button class="action-btn play" @click="playSongById(play.song_id)">
                  播放
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div class="empty-list" v-else>
          <p>暂无播放记录</p>
        </div>
      </div>
      
      <!-- 个人设置 -->
      <div v-if="activeTab === 2" class="user-settings">
        <h2>个人设置</h2>
        
        <form @submit.prevent="updateUserInfo" class="settings-form">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="userForm.username">
          </div>
          
          <div class="form-group">
            <label>邮箱</label>
            <input type="email" v-model="userForm.email">
          </div>
          
          <div class="form-group">
            <label>修改密码</label>
            <input type="password" v-model="userForm.password" placeholder="留空表示不修改">
          </div>
          
          <div class="form-group">
            <label>确认密码</label>
            <input type="password" v-model="userForm.confirmPassword" placeholder="留空表示不修改">
          </div>
          
          <div class="form-group">
            <label>头像</label>
            <input type="file" @change="onAvatarChange" accept="image/*">
          </div>
          
          <div class="form-actions">
            <button type="submit" class="save-btn">保存修改</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserPage',
  data() {
    return {
      user: {},
      activeTab: 0,
      tabs: [
        { name: '我的收藏' },
        { name: '最近播放' },
        { name: '个人设置' }
      ],
      favoriteSongs: [],
      recentPlays: [],
      userForm: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        avatar: null
      }
    };
  },
  created() {
    this.fetchUserData();
  },
  watch: {
    '$route.params.id': function() {
      this.fetchUserData();
    },
    activeTab() {
      this.loadTabData();
    }
  },
  methods: {
    fetchUserData() {
      const userId = this.$route.params.id;
      
      this.$axios.get(`/api/user/${userId}/`)
        .then(response => {
          this.user = response.data || {};
          
          // 初始化表单数据
          this.userForm.username = this.user.username || '';
          this.userForm.email = this.user.email || '';
          
          // 加载当前标签页数据
          this.loadTabData();
        })
        .catch(error => {
          console.error('获取用户数据失败:', error);
        });
    },
    loadTabData() {
      const userId = this.$route.params.id;
      
      switch (this.activeTab) {
        case 0: // 收藏歌曲
          this.$axios.get(`/api/user/${userId}/favorites/`)
            .then(response => {
              this.favoriteSongs = response.data || [];
            })
            .catch(error => {
              console.error('获取收藏歌曲失败:', error);
            });
          break;
          
        case 1: // 最近播放
          this.$axios.get(`/api/user/${userId}/recent-plays/`)
            .then(response => {
              this.recentPlays = response.data || [];
            })
            .catch(error => {
              console.error('获取最近播放记录失败:', error);
            });
          break;
      }
    },
    playSong(song) {
      this.$store.commit('setCurrentSong', song);
      this.$router.push(`/play/${song.id}`);
    },
    playSongById(songId) {
      this.$router.push(`/play/${songId}`);
    },
    removeFavorite(songId) {
      if (!confirm('确定要取消收藏这首歌曲吗？')) return;
      
      this.$axios.delete(`/api/user/favorites/${songId}/`)
        .then(() => {
          // 从列表中移除
          this.favoriteSongs = this.favoriteSongs.filter(song => song.id !== songId);
        })
        .catch(error => {
          console.error('取消收藏失败:', error);
        });
    },
    onAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.userForm.avatar = file;
      }
    },
    updateUserInfo() {
      // 验证密码
      if (this.userForm.password && this.userForm.password !== this.userForm.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }
      
      // 创建FormData对象
      const formData = new FormData();
      formData.append('username', this.userForm.username);
      formData.append('email', this.userForm.email);
      
      if (this.userForm.password) {
        formData.append('password', this.userForm.password);
      }
      
      if (this.userForm.avatar) {
        formData.append('avatar', this.userForm.avatar);
      }
      
      // 发送请求
      this.$axios.put(`/api/user/${this.user.id}/update/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          alert('个人信息更新成功');
          // 更新用户数据
          this.user = response.data;
          // 重置密码字段
          this.userForm.password = '';
          this.userForm.confirmPassword = '';
        })
        .catch(error => {
          console.error('更新用户信息失败:', error);
          alert('更新失败，请重试');
        });
    }
  }
};
</script>

<style scoped>
.user-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.user-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  margin-right: 20px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #eee;
}

.user-info h1 {
  margin-top: 0;
  margin-bottom: 10px;
}

.user-info p {
  margin: 5px 0;
  color: #666;
}

.user-tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border: 1px solid transparent;
  border-bottom: none;
  margin-right: 5px;
  border-radius: 4px 4px 0 0;
}

.tab.active {
  background-color: #fff;
  border-color: #ddd;
  border-bottom-color: #fff;
  margin-bottom: -1px;
  color: #1890ff;
  font-weight: bold;
}

.tab-content {
  min-height: 400px;
}

.tab-content h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

tr:hover {
  background-color: #f9f9f9;
}

.action-btn {
  padding: 6px 12px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.play {
  background-color: #1890ff;
  color: white;
}

.remove {
  background-color: #ff4d4f;
  color: white;
}

.empty-list {
  text-align: center;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.settings-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-actions {
  margin-top: 30px;
}

.save-btn {
  padding: 10px 20px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

a {
  color: #1890ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>