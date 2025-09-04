<template>
  <div class="index-page">
    <div class="header">
      <a href="/" class="logo">
        <img :src="logoUrl" alt="Logo">
      </a>
      <div class="search-box">
        <form @submit.prevent="searchSong">
          <div class="search-keyword">
            <input v-model="keyword" type="text" class="keyword" maxlength="120">
          </div>
          <button type="submit" class="search-button">搜 索</button>
        </form>
        <div class="search-hot-words">
          <a v-for="(song, index) in hotSearches" :key="index" 
             :href="`/play/${song.id}`" target="play">{{ song.name }}</a>
        </div>
      </div>
    </div>
    
    <div class="nav-box">
      <div class="nav-box-inner">
        <ul class="nav clearfix">
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/ranking">歌曲排行</router-link></li>
          <li><router-link to="/user/1">用户中心</router-link></li>
        </ul>
        
        <div class="category-nav">
          <div class="category-nav-header">
            <strong><a href="javascript:;" title="">音乐分类</a></strong>
          </div>
          <div class="category-nav-body">
            <ul>
              <li v-for="label in labels" :key="label.id">
                <a href="javascript:;">{{ label.name }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <div class="main-content">
      <div class="popular-songs">
        <h2>热门歌曲</h2>
        <ul>
          <li v-for="song in popularSongs" :key="song.id">
            <router-link :to="`/play/${song.id}`">{{ song.name }} - {{ song.singer }}</router-link>
            <span class="play-count">播放次数: {{ song.plays }}</span>
          </li>
        </ul>
      </div>
      
      <div class="recommend-songs">
        <h2>新歌推荐</h2>
        <ul>
          <li v-for="song in recommendSongs" :key="song.id">
            <router-link :to="`/play/${song.id}`">{{ song.name }} - {{ song.singer }}</router-link>
            <span class="release-date">发行日期: {{ song.release }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      logoUrl: '/static/image/logo.png',
      keyword: '',
      hotSearches: [],
      labels: [],
      popularSongs: [],
      recommendSongs: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.$axios.get('/api/index/data/')
        .then(response => {
          const data = response.data;
          this.hotSearches = data.searchs || [];
          this.labels = data.labels || [];
          this.popularSongs = data.popular || [];
          this.recommendSongs = data.recommend || [];
        })
        .catch(error => {
          console.error('获取数据失败:', error);
        });
    },
    searchSong() {
      if (this.keyword.trim()) {
        this.$router.push(`/search/1?kword=${encodeURIComponent(this.keyword)}`);
      }
    }
  }
};
</script>

<style scoped>
/* 可以引入或复用Django项目中的CSS样式 */
.index-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.logo img {
  height: 50px;
}

.search-box {
  margin-left: 20px;
  flex-grow: 1;
}

.search-keyword input {
  width: 300px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-button {
  padding: 8px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-hot-words {
  margin-top: 8px;
}

.search-hot-words a {
  margin-right: 10px;
  color: #666;
  text-decoration: none;
}

.nav-box {
  background-color: #f5f5f5;
  padding: 10px 0;
  margin-bottom: 20px;
}

.nav {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
}

.nav li {
  margin-right: 20px;
}

.nav a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.category-nav {
  margin-top: 10px;
}

.category-nav-body ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
}

.category-nav-body li {
  margin-right: 15px;
  margin-bottom: 5px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.popular-songs, .recommend-songs {
  background-color: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.popular-songs h2, .recommend-songs h2 {
  margin-top: 0;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.popular-songs ul, .recommend-songs ul {
  list-style: none;
  padding: 0;
}

.popular-songs li, .recommend-songs li {
  padding: 8px 0;
  border-bottom: 1px dashed #eee;
  display: flex;
  justify-content: space-between;
}

.play-count, .release-date {
  color: #999;
  font-size: 0.9em;
}
</style>