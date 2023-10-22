CREATE TABLE `ticket_order_monitor_show` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `show_id` varchar(255) NOT NULL DEFAULT '' COMMENT '演出id',
  `show_name` varchar(255) NOT NULL DEFAULT '' COMMENT '演出名称',
  `platform` int(11) NOT NULL DEFAULT '0' COMMENT '演出平台',
  `monitor_end_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '监控结束时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;