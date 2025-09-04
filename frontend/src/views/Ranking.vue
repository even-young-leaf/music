<template>
  <div class="ranking-page">
    <h1>歌曲排行榜</h1>
    
    <div class="ranking-tabs">
      <div class="tab" 
           v-for="(tab, index) in tabs" 
           :key="index"
           :class="{ active: activeTab === index }"
           @click="activeTab = index">
        {{ tab.name }}
      </div>
    </div>
    
    <div class="ranking-list">
      <table>
        <thead>
          <tr>
            <th>排名</th>
            <th>歌曲</th>
            <th>歌手</th>
            <th>{{ tabs[activeTab].metric }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(song, index) in songs" :key="song.id">
            <td class="rank">{{ index + 1 }}</td>
            <td>
              <router-link :to="`/play/${song.id}`">{{ song.name }}</router-link>
            </td>
            <td>{{ song.singer }}</td>
            <td>{{ song[tabs[activeTab].key] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RankingPage',
  data() {
    return {
      activeTab: 0,
      tabs: [
        { name: '播放排行', key: 'plays', metric: '播放次数' },
        { name: '下载排行', key: 'downloads', metric: '下载次数' },
        { name: '搜索排行', key: 'searches', metric: '搜索次数' }
      ],
      songs: []
    };
  },
  watch: {
    activeTab() {
      this.fetchRankingData();
    }
  },
  created() {
    this.fetchRankingData();
  },
  methods: {
    fetchRankingData() {
      const tabKey = this.tabs[this.activeTab].key;
      this.$axios.get(`/api/ranking/${tabKey}/`)
        .then(response => {
          this.songs = response.data || [];
        })
        .catch(error => {
          console.error('获取排行榜数据失败:', error);
        });
    }
  }
};
</script>

<style scoped>
.ranking-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.ranking-tabs {
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

.ranking-list table {
  width: 100%;
  border-collapse: collapse;
}

.ranking-list th, .ranking-list td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.ranking-list th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.ranking-list tr:hover {
  background-color: #f9f9f9;
}

.rank {
  font-weight: bold;
  width: 60px;
}

.rank:nth-child(1), .rank:nth-child(2), .rank:nth-child(3) {
  color: #ff4d4f;
}

a {
  color: #1890ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>