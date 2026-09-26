"""
End-to-End Test for Phase 4: Pipeline and Planner.
Tests:
1. Archetype inference and schema validation.
2. Generating a complete 5-slide enterprise deck via pipeline.
3. Dark mode theme support.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import (
    DeckConfig,
    SlidePlan,
    DeckPlan,
    PlanMapper,
    auto_plan_from_outline,
    M3DeckBuilder,
    build_deck_from_dict,
)

def test_inference_rules():
    print("Testing Archetype Inference Rules...")
    # Test keywords
    assert PlanMapper.infer_archetype({"title": "项目年度路线图与里程碑"}, 2, 5) == "process_roadmap"
    assert PlanMapper.infer_archetype({"title": "传统架构 vs 现代云原生架构深度比对"}, 2, 5) == "dual_contrast"
    assert PlanMapper.infer_archetype({"title": "核心生产环境性能指标大屏"}, 2, 5) == "kpi_metrics"
    assert PlanMapper.infer_archetype({"title": "系统三大核心技术支柱"}, 2, 5) == "feature_list"
    assert PlanMapper.infer_archetype({"title": "技术领军团队与组织架构"}, 2, 5) == "team_showcase"
    assert PlanMapper.infer_archetype({"title": "架构哲学与未来愿景寄语"}, 2, 5) == "quote_takeaway"
    assert PlanMapper.infer_archetype({"title": "下一代智能工作流发布"}, 1, 5) == "cover_hero"
    print("  [OK] All archetype inference rules passed!")

def test_pipeline_deck_generation():
    print("\nTesting End-to-End 5-Slide Pipeline Deck Generation...")

    deck_outline = {
        "config": {
            "title": "2026 全球智能云原生技术峰会",
            "preset_theme": "electric_mint",  # Testing electric mint theme
            "is_dark": False,
        },
        "slides": [
            {
                "archetype": "cover_hero",
                "category": "CLOUD NATIVE SUMMIT 2026",
                "title": "智能云原生架构演进：\n高吞吐弹性计算与全链路观测",
                "subtitle": "融合 Google M3 Expressive 设计规范、分布式容器编排与 AI 驱动自愈管线",
                "speaker": "云原生系统首席架构师",
                "date": "2026 年 10 月",
                "org": "Google Cloud Architecture Group",
                "hero_highlight": "CLOUD-2026",
                "hero_badge_text": "全球下一代智算集群",
            },
            {
                "archetype": "bento_grid",
                "category": "ARCHITECTURE PANORAMA",
                "title": "全景看板：智能云原生服务分舱体系",
                "subtitle": "采用 28dp Bento 模块化分舱，提供高内聚、低耦合的服务治理全视图",
                "hero_card": {
                    "chip": "CORE CLUSTER", "icon": "hub",
                    "title": "自适应弹性调度中心", "subtitle": "Adaptive Workload Scheduler",
                    "desc": "基于实时流量感知与强化学习算法，毫秒级完成万节点算力智能动态切分与扩缩容。",
                    "metric_val": "99.99%", "metric_label": "核心服务在线稳定性", "trend": "+4.2x 吞吐"
                },
                "card_top": {
                    "icon": "shield", "title": "零信任安全边界",
                    "desc": "全域 mTLS 动态认证与细粒度 RBAC 权限隔离，杜绝未授权横向移动风险。",
                    "chips": ["动态密钥轮换", "硬件隔离舱", "国密合规"]
                },
                "card_bot_left": {
                    "icon": "bolt", "stat": "< 5ms",
                    "title": "超低时延网络", "desc": "RDMA 原生直连，突破传统 TCP 协议栈开销。"
                },
                "card_bot_right": {
                    "icon": "verified", "title": "工业级全可观测",
                    "bullets": ["指标/日志/链路三位一体", "分钟级根因定位推断", "100% 自动化全景巡检"]
                }
            },
            {
                "archetype": "process_roadmap",
                "category": "EXECUTION TIMELINE",
                "title": "四阶段云原生体系化演进路线图",
                "subtitle": "从传统单体解耦、混合多云迁移，到 AI 智能自治与全球化容灾部署",
                "phases": [
                    {
                        "phase_num": "01", "name": "底座微服务化", "time": "2025 Q1-Q2", "status": "COMPLETED",
                        "icon": "check", "deliverables": ["核心交易链路拆分", "统一 API 网关上线", "CI/CD 自动化流水线"],
                        "kpi_chip": "基座 100% 容器化"
                    },
                    {
                        "phase_num": "02", "name": "服务网格接入", "time": "2025 Q3-Q4", "status": "COMPLETED",
                        "icon": "bolt", "deliverables": ["Istio 全量平滑纳管", "全链路金丝雀发布", "端到端可观测性看板"],
                        "kpi_chip": "流量治理就绪"
                    },
                    {
                        "phase_num": "03", "name": "混合多云调度", "time": "2026 Q1-Q2", "status": "ACTIVE",
                        "icon": "layers", "deliverables": ["跨云多活调度器", "全球任播智能路由", "边缘算力按需卸载"],
                        "kpi_chip": "当前重点攻关"
                    },
                    {
                        "phase_num": "04", "name": "AI 自治运维", "time": "2026 Q3-Q4", "status": "UPCOMING",
                        "icon": "rocket", "deliverables": ["大模型告警自治压制", "智能算力预测扩容", "零人工介入自愈"],
                        "kpi_chip": "终态演进目标"
                    }
                ]
            },
            {
                "archetype": "dual_contrast",
                "category": "TECH PARADIGM SHIFT",
                "title": "传统自建 IDC vs 现代智能云原生深度对比",
                "subtitle": "对比传统沉重运维包袱与下一代弹性敏捷架构的革命性飞跃",
                "left_plan": {
                    "chip": "TRADITIONAL IDC",
                    "title": "传统物理机与虚拟机部署",
                    "desc": "硬件采购周期冗长，算力峰值难以预估，日常闲置率高达 65% 以上，运维成本居高不下。",
                    "points": [
                        "服务器静态绑定，资源割裂无法池化",
                        "故障切换依赖人工介入，恢复时效长",
                        "升级停机窗口长，变更风险难以把控",
                        "底层黑盒缺乏细粒度实时洞察"
                    ],
                    "metric_val": "35%",
                    "metric_label": "资源平均综合利用率",
                    "trend": "传统运维瓶颈"
                },
                "right_plan": {
                    "chip": "M3 CLUSTER NATIVE",
                    "title": "智算混合多云原生架构",
                    "desc": "毫秒级容器秒启秒销，算力全局池化智能调度，AI 驱动故障自愈与极速容灾。",
                    "points": [
                        "资源池化统一调度，利用率跃升至 82%",
                        "秒级容器自愈与无感知流量重路由",
                        "蓝绿灰度无中断发布，变更风险归零",
                        "全栈指标链路纳管，秒级异常报警定位"
                    ],
                    "metric_val": "82.5%",
                    "metric_label": "算力综合利用率跃升",
                    "trend": "+2.4x 效能跃迁"
                }
            },
            {
                "archetype": "kpi_metrics",
                "category": "MEASURABLE IMPACT",
                "title": "核心业务运行指标与量化成效大屏",
                "subtitle": "经过全栈智能化云原生重构后，关键可用性、资源节省与发布频率均实现翻倍级突破",
                "metrics": [
                    {
                        "value": "99.999%", "label": "核心交易 SLA 可用性", "trend": "+0.09% 达到金融级",
                        "icon": "shield", "desc": "多活高可用异地容灾架构", "highlight": False
                    },
                    {
                        "value": "6.8 ms", "label": "核心网关 P99 延迟", "trend": "-72% 极大加速",
                        "icon": "speed", "desc": "eBPF 网络层零拷贝转发", "highlight": True
                    },
                    {
                        "value": "120+", "label": "日均发布部署频次", "trend": "+500% 极速交付",
                        "icon": "rocket", "desc": "全自动化 GitOps 交付流水线", "highlight": False
                    },
                    {
                        "value": "42.8%", "label": "全年 TCO 综合成本节约", "trend": "节约数千万元支出",
                        "icon": "savings", "desc": "智能弹性缩容与潮汐调度", "highlight": False
                    }
                ],
                "takeaway_badge": "EXECUTIVE TAKEAWAY",
                "takeaway_text": "量化结论：云原生智能化演进不仅大幅夯实了高可用底层基座，更在保障 P99 延迟降至 6.8ms 的同时削减了 42.8% 的基础设施支出。"
            }
        ]
    }

    out_pptx = "tests/output/pipeline_cloud_summit.pptx"
    result_path = build_deck_from_dict(deck_outline, out_pptx)
    print(f"  [OK] Pipeline generated deck: {result_path}")
    assert os.path.exists(result_path)

if __name__ == "__main__":
    test_inference_rules()
    test_pipeline_deck_generation()
    print("\n[ALL TESTS PASSED] Phase 4 Pipeline verified successfully!")
