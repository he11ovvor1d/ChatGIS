var map = new BMapGL.Map("container");          // 创建地图实例 
var point = new BMapGL.Point(116.404, 39.915);  // 创建点坐标 
map.centerAndZoom(point, 15);                 // 初始化地图，设置中心点坐标和地图级别
map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
map.setHeading(64.5);   //设置地图旋转角度
map.setTilt(73);       //设置地图的倾斜角度

// 禁止地图旋转和倾斜可以通过配置项进行设置
var map = new BMapGL.Map("allmap",{
    enableRotate: false,
    enableTilt: false
});