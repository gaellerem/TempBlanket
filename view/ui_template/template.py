from string import Template

def make_ui():
    with open('view/ui_template/template.txt', 'r') as f:
        template = Template(f.read())

    spinboxes = ''
    with open('datas/color_pairs.csv', 'r') as f:
        for i, line in enumerate(f):
            if i == 0: continue
            line = line.strip().split(';')
            spinboxes += f"""
            <item>
            <widget class="QWidget" name="widget_{i}" native="true">
                <layout class="QHBoxLayout" name="horizontalLayout_{i}">
                    <property name="leftMargin">
                        <number>0</number>
                    </property>
                    <property name="topMargin">
                        <number>0</number>
                    </property>
                    <property name="rightMargin">
                        <number>0</number>
                    </property>
                    <property name="bottomMargin">
                        <number>0</number>
                    </property>
                <item>
                    <widget class="QLabel" name="label_{i}">
                        <property name="maximumSize">
                            <size>
                                <width>75</width>
                                <height>75</height>
                            </size>
                        </property>
                        <property name="toolTip">
                            <string>{line[1]}_{line[2]}</string>
                        </property>
                        <property name="text">
                            <string/>
                        </property>
                        <property name="pixmap">
                            <pixmap resource="resource.qrc">:/pairs/assets/{line[1]}_{line[2]}.png</pixmap>
                        </property>
                        <property name="scaledContents">
                            <bool>true</bool>
                        </property>
                    </widget>
                </item>
                <item>
                    <widget class="QSpinBox" name="spinBox_{i}">
                    <property name="maximumSize">
                    <size>
                    <width>50</width>
                    <height>16777215</height>
                    </size>
                    </property>
                    <property name="minimum">
                    <number>0</number>
                    </property>
                    <property name="maximum">
                    <number>{int(line[0])}</number>
                    </property>
                    </widget>
                </item>
                <item>
                    <widget class="QLabel" name="label_{i}_2">
                        <property name="text">
                        <string>/{line[0]}</string>
                        </property>
                    </widget>
                </item>
            </layout>
            </widget>
            </item>"""
    with open('view/ui/main.ui', 'w', encoding="utf-8") as f:
        f.write(template.substitute(spinboxes=spinboxes))
