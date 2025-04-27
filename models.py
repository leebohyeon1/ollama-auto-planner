"""
데이터 모델 정의
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any


@dataclass
class CodeSnippet:
    """코드 스니펫 모델"""
    language: str
    code: str
    description: Optional[str] = None
    filename: Optional[str] = None
    
    def save_to_file(self, base_dir: str) -> str:
        """코드 스니펫을 파일로 저장합니다."""
        import os
        
        if not self.filename:
            lang_ext = {
                "python": "py",
                "javascript": "js",
                "typescript": "ts",
                "java": "java",
                "cpp": "cpp",
                "c": "c",
                "csharp": "cs",
                "go": "go",
                "rust": "rs",
                "ruby": "rb",
                "php": "php",
                "swift": "swift",
                "kotlin": "kt",
                "text": "txt",
                "": "txt"
            }
            
            # 언어 확장자 찾기, 없으면 기본값 txt 사용
            ext = lang_ext.get(self.language.lower(), "txt")
            self.filename = f"snippet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
        
        file_path = os.path.join(base_dir, self.filename)
        
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.code)
        
        return file_path


@dataclass
class Feature:
    """기능 모델"""
    name: str
    description: str
    priority: str = "medium"  # 우선순위: high, medium, low
    complexity: str = "medium"  # 복잡도: high, medium, low
    status: str = "proposed"  # 상태: proposed, in_progress, completed
    code_snippets: List[CodeSnippet] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """객체를 사전 형태로 변환합니다."""
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "complexity": self.complexity,
            "status": self.status,
            "code_snippets": [
                {
                    "language": snippet.language,
                    "code": snippet.code,
                    "description": snippet.description,
                    "filename": snippet.filename
                }
                for snippet in self.code_snippets
            ],
            "dependencies": self.dependencies
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feature':
        """사전 형태의 데이터에서 객체를 생성합니다."""
        code_snippets = [
            CodeSnippet(
                language=snippet.get("language", ""),
                code=snippet.get("code", ""),
                description=snippet.get("description"),
                filename=snippet.get("filename")
            )
            for snippet in data.get("code_snippets", [])
        ]
        
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            complexity=data.get("complexity", "medium"),
            status=data.get("status", "proposed"),
            code_snippets=code_snippets,
            dependencies=data.get("dependencies", [])
        )


@dataclass
class Component:
    """컴포넌트 모델"""
    name: str
    description: str
    features: List[Feature] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """객체를 사전 형태로 변환합니다."""
        return {
            "name": self.name,
            "description": self.description,
            "features": [feature.to_dict() for feature in self.features]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        """사전 형태의 데이터에서 객체를 생성합니다."""
        features = [Feature.from_dict(feature_data) for feature_data in data.get("features", [])]
        
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            features=features
        )


@dataclass
class Project:
    """프로젝트 모델"""
    name: str
    description: str
    components: List[Component] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """객체를 사전 형태로 변환합니다."""
        return {
            "name": self.name,
            "description": self.description,
            "components": [component.to_dict() for component in self.components],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """사전 형태의 데이터에서 객체를 생성합니다."""
        components = [Component.from_dict(component_data) for component_data in data.get("components", [])]
        
        created_at = datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else datetime.now()
        updated_at = datetime.fromisoformat(data.get("updated_at")) if data.get("updated_at") else datetime.now()
        
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            components=components,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def save_to_json(self, file_path: str) -> None:
        """프로젝트를 JSON 파일로 저장합니다."""
        import json
        import os
        
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_json(cls, file_path: str) -> 'Project':
        """JSON 파일에서 프로젝트를 로드합니다."""
        import json
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
