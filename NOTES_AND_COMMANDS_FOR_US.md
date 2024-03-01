# to create additional services with grcp_tools
 python -m grpc_tools.protoc -Iutils/pb/suggestions_service --python_out=utils/pb/suggestions_service --pyi_out=utils/pb/suggestions_service --grpc_python_out=utils/pb/suggestions_service utils/pb/suggestions_service/suggestions_service.proto
