NCCL_PROCESS_IP="xxx"
NS3_PROCESS_IP="xxx"

# ---------------------------------------------------------------------------
# Files referenced by the mpirun command below. All paths are RELATIVE to this
# script's directory (the SimAI-CLEM root), so launch the script from there.
#
#   ./node2hca_map.conf            (env: SIMHCA2REALHCA_MAP_FILENAME)
#       Maps each simulated HCA (the ns-3 virtual NIC "ns3_qbbdev") to its real
#       HCA/port identity, so emulated RDMA traffic is routed onto the correct
#       simulated NIC in ns-3. Copied into the SimAI-CLEM root from
#       simulator-network/simulation/mix/node2hca_map.conf.
#
#   ./graph_info_1.xml             (env: SIM_CHANNEL_FILE)
#       Pre-computed NCCL topology / channel graph (rings & trees) consumed by
#       the emulator to set up the collective communication for this run.
#
#   ./nccl_hack_rdma/build/lib/libnccl.so.2   (env: LD_PRELOAD)
#       The SimAI-CLEM-modified NCCL shared library. Preloading it intercepts NCCL's
#       P2P/RDMA primitives and redirects them to the ns-3 simulator.
#       Rebuild from nccl + nccl_patch (see README, Quick Start Step 1-2).
#
#   ./nccl-tests-modify/build/all_reduce_perf
#       The instrumented nccl-tests all_reduce benchmark executable that drives
#       the collective operation under emulation. Rebuild from nccl-tests +
#       nccl_tests_patch (see README, Quick Start Step 4).
#
#   ./demo_16A100_allreduce_64MB.log          (tee output)
#       Console log captured from this 16x A100, 64MB all_reduce demo run.
# ---------------------------------------------------------------------------

mpirun --allow-run-as-root -H ${NCCL_PROCESS_IP}:16 -np 16 --map-by ppr:16:node \
       --mca btl_openib_warn_no_device_params_found 0 --mca btl_tcp_if_include bond0 \
        -x NCCL_PROTO=Simple -x NCCL_IB_SPLIT_DATA_ON_QPS=1 -x NCCL_NET_PLUGIN=0 \
        -x NCCL_IB_SL=5 -x NCCL_IB_TC=136 -x NCCL_IB_TIMEOUT=22 -x NCCL_IB_HCA=ns3_qbbdev \
        -x NCCL_IB_GID_INDEX=3 -x NCCL_ALGO=ring   -x NCCL_IB_QPS_PER_CONNECTION=8 \
        -x NCCL_DEBUG_SUBSYS=tuning,init,graph,net -x NCCL_DEBUG=INFO \
        -x NCCL_P2P_DISABLE=1 -x NCCL_SHM_DISABLE=1 \
        -x SIMU_ENABLE_GPU_P2P=true -x NUM_GPUS_PER_SERVER=8 \
        -x SIMHCA2REALHCA_MAP_FILENAME=./node2hca_map.conf \
        -x SIM_CHANNEL_FILE=./graph_info_1.xml \
        -x SIM_AVOID_CROSS_RAIL=1 -x START_NODE_ID=0 \
        -x LD_PRELOAD=./nccl_hack_rdma/build/lib/libnccl.so.2 \
        ./nccl-tests-modify/build/all_reduce_perf       -A ${NS3_PROCESS_IP} -b 64MB -e 64MB -f 2 -g 1 -w 0 -n 1 -c 0 | tee ./demo_16A100_allreduce_64MB.log
