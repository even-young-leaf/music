<template>
  <div class="search-page">
    <div class="search-header">
      <h1>搜索结果: "{{ keyword }}"</h1>
      <div class="search-form">
        <input 
          type="text" 
          v-model="keyword" 
          placeholder="输入关键词搜索"
          @keyup.enter="search"
        >
        <button @click="search">搜索</button>
      </div>
    </div>
    
    <div class="search-results" v-if="songs.length > 0">
      <table>
        <thead>
          <tr>
            <th>歌曲</th>
            <th>歌手</th>
            <th>专辑</th>
            <th>时长</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="song in songs" :key="song.id">
            <td>
              <router-link :to="`/play/${song.id}`">{{ song.name }}</router-link>
            </td>
            <td>{{ song.singer }}</td>
            <td>{{ song.album }}</td>
            <td>{{ formatDuration(song.time) }}</td>
            <td>
              <button class="action-btn play" @click="playSong(song)">
                播放
              </button>
              <button class="action-btn add" @click="addToPlaylist(song)">
                加入列表
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="pagination">
        <button 
          :disabled="currentPage <= 1" 
          @click="goToPage(currentPage - 1)"
          class="page-btn"
        >
          上一页
        </button>
        
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        
        <button 
          :disabled="currentPage >= totalPages" 
          @click="goToPage(currentPage + 1)"
          class="page-btn"
        >
          下一页
        </button>
      </div>
    </div>
    
    <div class="no-results" v-else>
      <p>未找到与 "{{ keyword }}" 相关的歌曲</p>
      <p>建议：</p>
      <ul>
        <li>请检查您的拼写</li>
        <li>尝试使用不同的关键词</li>
        <li>尝试使用更通用的关键词</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchPage',
  data() {
    return {
      keyword: '',
      songs: [],
      currentPage: 1,
      totalPages: 1,
      pageSize: 10
    };
  },
  created() {
    // 从URL获取搜索关键词和页码
    const { kword } = this.$route.query;
    this.currentPage = parseInt(this.$route.params.page) || 1;
    
    if (kword) {
      this.keyword = decodeURIComponent(kword);
      this.fetchSearchResults();
    }
  },
  watch: {
    '$route.params.page': function() {
      this.currentPage = parseInt(this.$route.params.page) || 1;
      this.fetchSearchResults();
    },
    '$route.query.kword': function() {
      const { kword } = this.$route.query;
      if (kword) {
        this.keyword = decodeURIComponent(kword);
        this.fetchSearchResults();
      }
    }
  },
  methods: {
    fetchSearchResults() {
      if (!this.keyword) return;
      
      this.$axios.get('/api/search/', {
        params: {
          kword: this.keyword,
          page: this.currentPage,
          page_size: this.pageSize
        }
      })
        .then(response => {
          this.songs = response.data.songs || [];
          this.totalPages = response.data.total_pages || 1;
        })
        .catch(error => {
          console.error('搜索失败:', error);
        });
    },
    search() {
      if (!this.keyword.trim()) return;
      
      // 重置页码并更新URL
      this.$router.push({
        path: '/search/1',
        query: { kword: this.keyword }
      });
    },
    goToPage(page) {
      if (page < 1 || page > this.totalPages) return;
      
      this.$router.push({
        path: `/search/${page}`,
        query: { kword: this.keyword }
      });
    },
    formatDuration(seconds) {
      if (!seconds) return '00:00';
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    playSong(song) {
      this.$store.commit('setCurrentSong', song);
      this.$router.push(`/play/${song.id}`);
    },
    addToPlaylist(song) {
      this.$store.commit('addToPlaylist', song);
      alert('已添加到播放列表');
    }
  }
};
</script>

<style scoped>
.search-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  margin-bottom: 30px;
}

.search-header h1 {
  margin-bottom: 15px;
}

.search-form {
  display: flex;
}

.search-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
}

.search-form button {
  padding: 10px 20px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
}

.search-results table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.search-results th, .search-results td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.search-results th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.search-results tr:hover {
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

.add {
  background-color: #52c41a;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.page-btn {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  margin: 0 15px;
  font-size: 16px;
}

.no-results {
  text-align: center;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.no-results p {
  margin-bottom: 15px;
}

.no-results ul {
  display: inline-block;
  text-align: left;
}

a {
  color: #1890ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>