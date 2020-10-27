from conans import ConanFile, tools, CMake


class FramelessHelperConan(ConanFile):
	name = "FramelessHelper"
	version = "0.1"
	license = "MIT"
	url = "https://github.com/wangwenx190/framelesshelper"
	settings = "os", "arch", "compiler", "build_type"
	description = "Frameless windows for Qt Widgets and Qt Quick applications. Support Win32, X11, Wayland and macOS."
	
	options = {"with_qtquick": [True, False]}
	default_options = {"with_qtquick": False}

	exports_sources = (
		"CMakeLists.txt",
		"*.h",
		"*.cpp",
		"framelesshelper.rc",
	)


	def _try_found_qt(self):
		qt_root = tools.get_env("QT_ROOT", "")
		if qt_root is None:
			raise RuntimeError("QT_ROOT env must be set")
		return qt_root


	def build(self):
		tools.replace_in_file("CMakeLists.txt",
			"cmake_minimum_required(VERSION 3.18)",
			"cmake_minimum_required(VERSION 3.16)")

		if not self.options.with_qtquick:
			tools.replace_in_file("CMakeLists.txt",
				"find_package(Qt5 COMPONENTS Widgets Quick)",
				"find_package(Qt5 COMPONENTS Widgets)")

		cmake = CMake(self)
		cmake.definitions["BUILD_SHARED_LIBS"] = False
		cmake.definitions["CMAKE_PREFIX_PATH"] = self._try_found_qt()
		cmake.configure()
		cmake.build()


	def package(self):
		self.copy("framelesshelper_global.h", dst="include", src=self.source_folder)
		self.copy("framelesswindowsmanager.h", dst="include", src=self.source_folder)
		self.copy("*.lib", dst="lib", keep_path=False)
		self.copy("*.so", dst="lib", keep_path=False)
		self.copy("*.dylib", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)


	def package_info(self):
		self.cpp_info.libs = tools.collect_libs(self)
		self.cpp_info.defines = ['FRAMELESSHELPER_STATIC']

		if self.settings.os == "Windows":
			self.cpp_info.system_libs = ["dwmapi", "shcore", "d2d1", "uxtheme"]
